import logging
import pandas as pd
import mmap
import struct
from datetime import datetime, timedelta
import numpy as np
import re

# import warnings
import pytz

# --- to be implemented in pipeline
# path_log=""

# codestartdate = str(datetime.datetime.today().strftime("%Y_%m_%d %H_%M"))

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[logging.FileHandler(path_log + "\\events_" + codestartdate + ".log")],
# )
# ---
rec_columns = {
    "Index": "record_ID",
    "Cycle No": "cycle",
    "Work Step No": "step_ID",
    "Work Step Name": "step_name",
    "Total Time": "timestamp",
    "Time Consuming": "time_in_step",
    "Voltage (mV)": "voltage_V",
    "Current (mA)": "current_mA",
    "Capacity (mAh)": "capacity_mAh",
    "Energy (mWh)": "energy_mWh",
    "Validation": "Validated",
}


ILLEGAL_CHARACTERS_RE = re.compile(r"[\000-\010]|[\013-\014]|[\016-\037]")
# if the pattern is 12345 ['Rest', 'CCCV-C', 'CC-D']
state_dict = {
    1: "Rest",
    2: "CCCV-C",
    3: "Rest",
    4: "CC-D",
    5: "Rest",
    6: "CCCV-C",
    7: "Rest",
    8: "end",
}
dtype_dict = {
    "Total Time": "int",
    "Voltage (mV)": "int",
    "Current (mA)": "int",
    "Capacity (mAh)": "float",
    "Energy (mWh)": "float",
}


def _single_validator(list):

    if list[0] < 0 or list[1] < 0 or list[3] < 0 or list[5] < 1.5:
        return False
    return True


def _validate_timegap(df1):

    df1.loc[
        (df1["Total Time"].diff() > 0),
        "Validated",
    ] = True


def _powercutgap(df2):
    list = df2["Work Step No"].unique()
    mask = df2.groupby(by="Work Step No")["Current (mA)"].agg(pd.Series.mode)
    rest_bucket = []
    for i in list:
        if (mask[i] == 0).any():
            rest_bucket.append(i)

    res = df2.groupby("Work Step No")["Time Consuming"].agg(last="last")
    n = res.shape[0]
    for i in range(1, n + 1):
        if i not in rest_bucket:
            df = df2.groupby(by="Work Step No").get_group(i)
            idx = df[
                (df["Current (mA)"] == 0)
                & (df["Time Consuming"].diff() == 0)
                & (df["Time Consuming"] != res["last"][i])
            ].index.values
            if idx.shape[0] != 0:
                # print("There is powercut at {0} index".format(idx+1))
                if (df.loc[idx[0] - 1, "Current (mA)"] == 0).any():
                    idx = np.insert(idx, 0, idx[0] - 1)
                logging.warning("There is powercut at {0} index".format(idx))


def _powercutgapremove(df2):
    list = df2["Work Step No"].unique()
    mask = df2.groupby(by="Work Step No")["Current (mA)"].agg(pd.Series.mode)
    rest_bucket = []
    for i in list:
        if (mask[i] == 0).any():
            rest_bucket.append(i)

    res = df2.groupby("Work Step No")["Time Consuming"].agg(last="last")
    l = res.shape[0]
    # res
    for i in range(1, l + 1):
        if i not in rest_bucket:
            df = df2.groupby(by="Work Step No").get_group(i)
            df2.drop(
                df[
                    (df["Current (mA)"] == 0)
                    & (df["Time Consuming"].diff() == 0)
                    & (df["Time Consuming"] != res["last"][i])
                ].index,
                inplace=True,
            )


def _main_validation(df):
    """Recipe validation"""

    #  Rest Status validation
    list = df["Work Step No"].unique()
    mask = df.groupby(by="Work Step No")["Current (mA)"].agg(pd.Series.mode)
    rest_bucket = []
    for i in list:
        if (mask[i] == 0).any():
            rest_bucket.append(i)
        if (mask[i] == 0).any() and df.groupby(by="Work Step No")[
            "Work Step Name"
        ].get_group(i).unique() != "Rest":
            #     if mask[step] == 0 and 'Rest' not in df1[df1['Work Step No'] == step]['Work Step Name'].unique():
            logging.warning("Status is mismatched for Work Step No: {}".format(i))

    #  Charge and discharge condition status
    """
     Filter data according to time consuming and also remove all 0 current rows from CCCV-C and CC-D
     """
    df1 = df.drop(
        df[(df["Current (mA)"] == 0) & (df["Work Step Name"] == "CC-D")].index
    )
    df1 = df.drop(
        df[(df["Current (mA)"] == 0) & (df["Work Step Name"] == "CCCV-C")].index
    )

    res = df1.groupby("Work Step No")["Voltage (mV)"].agg(first="first", last="last")
    for i in df1["Work Step No"].unique():
        if i not in rest_bucket:
            if (res.loc[i, "first"] - res.loc[i, "last"]) < 0:
                # print(i,"  ",df1.groupby(by ='Work Step No')['Work Step Name'].get_group(i).unique())
                if (
                    df1.groupby(by="Work Step No")["Work Step Name"]
                    .get_group(i)
                    .unique()
                    != "CCCV-C"
                ):
                    print("The state of CCCV charging is incorrect.")
            if (res.loc[i, "first"] - res.loc[i, "last"]) > 0:
                # print(i," ",df1.groupby(by ='Work Step No')['Work Step Name'].get_group(i).unique())
                if (
                    df1.groupby(by="Work Step No")["Work Step Name"]
                    .get_group(i)
                    .unique()
                    != "CC-D"
                ):
                    print("CC discharge but status is wrong")

    if len(df[df["Work Step No"].diff() < 0]):
        logging.warning("The assignment of the Work Step Number is not accurate.")
    if len(df[df["Total Time"].diff() < 0]):
        logging.warning("Total time diff is negative")
    if len(df[df["Index"].diff() < 1]):
        logging.warning("Index error")
    if len(df[df["Cycle No"].diff() < 0]):
        logging.warning("Cycle error")

    # #  Capacity (mAh) check
    if (
        (df1["Work Step Name"] == "Rest")
        & (df1["Current (mA)"] == 0)
        & (df1["Capacity (mAh)"] != 0.00)
    ).any():
        logging.warning("Capacity decoded incorrectly, Please check the file version.")

    if (
        (df1["Work Step Name"] == "Rest")
        & (df1["Current (mA)"] == 0)
        & (df1["Energy (mWh)"] != 0.00)
    ).any():
        logging.warning("Energy decoded incorrectly, Please check the file version.")


def _byte_to_list(bytes):
    #  Extract fields from byte string
    # [len] = struct.unpack('B',bytes[0:1])
    [number, cycle, v2] = struct.unpack("<BBB", bytes[10:13])
    [vol, curr] = struct.unpack("ff", bytes[15:23])
    [cap, eng] = struct.unpack("II", bytes[31:39])
    [time] = struct.unpack("H", bytes[46:48])
    [tis] = struct.unpack(
        "<H", bytes[39:41]
    )  # time in step - status wise time consuming
    # [tis]=struct.unpack('<H',bytes[39:41])

    list = [
        cycle,
        number,
        state_dict[number],
        time,
        tis,
        vol,
        curr,
        cap / 100,
        eng / 100,
        # tis,
    ]
    list.append(_single_validator(list))
    return list


def get_barcode(file):

    if file.split(".")[-1] != "rtd":
        raise ValueError("File passed in function is not an rtd file")

    with open(file, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        bytes = mm.read()
        # can add validatiton with the first element for length
        code = bytes[36:61][1:].decode("utf-8")
        if ILLEGAL_CHARACTERS_RE.search(code):
            return logging.warning("The given barcode value is inaccurate.")

        if re.search("[~!#$%^&*()_+{}:;']+$", code):
            logging.warning("Barcode has illegal character please check file")
    return code


def get_batchname(file):

    if file.split(".")[-1] != "rtd":
        raise ValueError("File passed in function is not an rtd file")

    with open(file, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        bytes = mm.read()
        # can add validatiton with the first element for length
        batch_ = bytes[76:100][1:].decode("utf-8")
        if ILLEGAL_CHARACTERS_RE.search(batch_):
            # if re.match("[~!#$%^&*()_+{}:;\']+$",code)
            return logging.warning("The provided barcode value is incorrect.")
    return batch_


def read(
    file,
    rename: bool = True,
    min_three_step: bool = False,
    keep_data_ac_recipe_time: bool = False,
):
    """
    Args: file - rtd file with .rtd extention

    Args: rename the File if rename=True

    Args: min_three_step - Check if file has at least ['Rest', 'CCCV-C', 'CC-D'] steps

    Args: keep_data_ac_recipe - keep it  false, you may loose the meaningful data

    Returns the Dataframe record-wise.

    """
    if file.split(".")[-1] != "rtd":
        raise ValueError("File passed in function is not an rtd file")

    with open(file, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        bytes = mm.read()
        start_time, end_time = struct.unpack("QQ", bytes[4:20])
        # start_time = datetime.utcfromtimestamp(start_time // 1000).strftime(
        # "%Y-%m-%d %H:%M:%S"
        # )
        end_time = (
            datetime.fromtimestamp(end_time // 1000)
            .replace(tzinfo=pytz.UTC)
            .strftime("%Y-%m-%d %H:%M:%S")
        )
        # utcfromtimestamp is deprecated
        start_time = (
            datetime.fromtimestamp(start_time // 1000)
            .replace(tzinfo=pytz.UTC)
            .strftime("%Y-%m-%d %H:%M:%S")
        )
        # start_time = start_time.replace(tzinfo=pytz.UTC)
        # start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')

        # end_time = datetime.fromtimestamp(end_time//1000).strftime('%Y-%m-%d %H:%M:%S')
        [n] = struct.unpack("B", bytes[802:803])
        check = bytes[803 : 803 + n]
        rec = []
        identifier = 3203
        mm.seek(identifier - 8)
        start = mm.tell()
        while mm.tell() < mm.size():
            len = mm.read_byte()
            end = mm.tell()
            # end=mm.seek(mm.tell()+len-1)
            if bytes[start + 7 : start + 10] == b"\xf8\xd8@":
                rec.append(_byte_to_list(bytes[start:]))
            start = mm.tell()
    df = pd.DataFrame(
        rec,
        columns=[
            "Cycle No",
            "Work Step No",
            "Work Step Name",
            "Total Time",
            "Time Consuming",
            "Voltage (mV)",
            "Current (mA)",
            "Capacity (mAh)",
            "Energy (mWh)",
            "Validation",
        ],
    )

    df["Date Time"] = pd.to_timedelta(
        df["Total Time"].astype("str") + "s"
    ) + pd.to_datetime(start_time)

    # check this with all the available files
    if check == b"12345" or check == b"12345CAP":
        pass
    else:
        print(
            "Please check the recipe. Work Step Number is define according to previous recipe."
        )

    if "DCIR(mOhm)" not in df.keys():
        # df.loc[((df['Current'].diff()==0)&(df['Current']!=0)),'DCIR(mOhm)']=(abs((df['Voltage'].diff()) /(df['Current'].diff())))

        df["prev_cur"] = df["Current (mA)"].shift(periods=1)
        df["prev_vol"] = df["Voltage (mV)"].shift(periods=1)
        df["DCIR(mOhm)"] = -1.0
        df.loc[((df["prev_cur"] == 0) & (df["Current (mA)"] != 0)), "DCIR(mOhm)"] = (
            abs(
                (df["Voltage (mV)"] - df["prev_vol"])
                / (df["Current (mA)"] - df["prev_cur"])
            )
            * 1000000
        )
        df.drop(columns=["prev_cur", "prev_vol"], inplace=True)
    # make sure total time is increasing
    if keep_data_ac_recipe_time:
        df.drop_duplicates(
            ["Work Step No", "Time Consuming(Recipe wise)"], keep="first", inplace=True
        )
        df.drop(
            df[
                (df["Current (mA)"] == 0)
                & (df["Work Step Name"] == "CC-D")
                & (df["Time Consuming"] != 0)
            ].index,
            inplace=True,
        )
        df.drop(
            df[
                (df["Current (mA)"] == 0)
                & (df["Work Step Name"] == "CCCV-C")
                & (df["Time Consuming"] != 0)
            ].index,
            inplace=True,
        )

    # drop duplicates from datatime or time in step in same step
    df.drop_duplicates(["Total Time", "Work Step No"], keep="first", inplace=True)

    var = df[df["Total Time"].diff() < 0].shape[0]
    for i in range(var):
        df = df[df["Total Time"].diff().fillna(0) >= 0]
    idx = df[df["Total Time"].diff() < 0].index.values
    try:
        if idx.shape[0]:
            removeall = [i for i in range(idx[idx.shape[0] - 1])]
            df.drop(removeall, inplace=True)
    except:
        pass

    df.drop(df[df["Total Time"].diff() < 1].index, inplace=True)

    try:
        if idx.shape[0]:
            removeall = [i for i in range(idx[idx.shape[0]])]
            df.drop(removeall, inplace=True)
    except:
        pass

    df.drop(df[df["Total Time"].diff() < 1].index, inplace=True)

    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.insert(loc=0, column="Index", value=df.index + 1)
    df = df.astype(dtype=dtype_dict)

    if min_three_step:
        if (
            df["Work Step Name"].unique().shape[0]
            != np.array(["Rest", "CCCV-C", "CC-D"]).shape[0]
        ):
            logging.warning(
                "The provided file does not contain an adequate number of steps."
            )

    _main_validation(df)
    # powercutgapremove(df)
    _powercutgap(df)

    if rename:
        df = df.rename(columns=rec_columns)

    return df
