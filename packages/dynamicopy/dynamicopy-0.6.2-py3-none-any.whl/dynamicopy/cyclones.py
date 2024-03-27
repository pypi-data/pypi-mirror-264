import pandas as pd
from datetime import datetime
import pickle as pkl
import pkg_resources
from .basins import *
from shapely.geometry import Point
from haversine import haversine_vector, Unit

"""
Format for loading the tracks _data : 
track_id    time                lon     lat     hemisphere  basin   season  sshs    slp     wind10  year    month   day     (wind925)
str         np.datetime64[ns]   float   float   str         str     str     int     float   float   int     int     int     (float)

0 <= lon <= 360
"""


def clean_ibtracs(
    raw_file="tests/ibtracs.since1980.list.v04r00_05092021.csv",
    csv_output="dynamicopy/_data/ibtracs.since1980.cleaned.csv",
    pkl_output="dynamicopy/_data/ibtracs.pkl",
):
    """
    Function used to post-treat ibtracs _data into a lighter file

    Parameters
    ----------
    raw_file: The csv file from the ibtracs database
    csv_output: The name of the csv file to be saved
    pkl_output: The name of the pickle file to be saved

    Returns
    -------
    The cleaned dataset
    + saves csv and pkl file
    """

    ib = pd.read_csv(
        raw_file,
        na_values=["", " "],
        header=0,
        skiprows=[1],
        usecols=[
            "SID",
            "SEASON",
            "BASIN",
            "SUBBASIN",
            "ISO_TIME",
            "NATURE",
            "TRACK_TYPE",
            "LON",
            "LAT",
            "USA_SSHS",
            "WMO_WIND",
            "USA_WIND",
            "TOKYO_WIND",
            "CMA_WIND",
            "REUNION_WIND",
            "BOM_WIND",
            "NADI_WIND",
            "WELLINGTON_WIND",
            "WMO_PRES",
            "USA_PRES",
            "TOKYO_PRES",
            "CMA_PRES",
            "HKO_PRES",
            "NEWDELHI_PRES",
            "REUNION_PRES",
            "BOM_PRES",
            "NADI_PRES",
            "WELLINGTON_PRES",
        ],
        converters={
            "SID": str,
            "SEASON": int,
            "BASIN": str,
            "SUBBASIN": str,
            "LON": float,
            "LAT": float,
        },
        parse_dates=["ISO_TIME"],
    )
    ib = ib[~ib.TRACK_TYPE.str.startswith("spur")]
    ib = ib[ib.SEASON < 2020]
    ib = ib[(ib.SEASON > 1980) | (ib.LAT > 0)]
    ib["WIND10"] = np.where(
        ~ib.WMO_WIND.isna(),
        ib.WMO_WIND,
        ib[
            ["TOKYO_WIND", "REUNION_WIND", "BOM_WIND", "NADI_WIND", "WELLINGTON_WIND"]
        ].mean(axis=1, skipna=True),
    )
    ib["WIND10"] = np.where(
        ib.WIND10.isna(), ib.USA_WIND / 1.12, ib.WIND10
    )  # Conversion rate in the IBTrACS doc
    ib["WIND10"] = np.where(
        ib.WIND10.isna(), ib.CMA_WIND / 1.08, ib.WIND10
    )  # Conversion rate determined through a linear regression
    ib["WIND10"] *= 0.514  # Conversion noeuds en m/s
    tcs = (
        ib.groupby("SID")["WIND10"].max()[ib.groupby("SID")["WIND10"].max() >= 17].index
    )
    ib = ib[ib.SID.isin(tcs)]  # Filter tracks not reaching 17 m/s
    tcs = (
        ib.groupby("SID")["ISO_TIME"]
        .count()[ib.groupby("SID")["ISO_TIME"].count() >= 4]
        .index
    )
    ib = ib[ib.SID.isin(tcs)]  # Filter tracks not reaching 17 m/s
    ib["PRES"] = np.where(
        ~ib.WMO_PRES.isna(),
        ib.WMO_PRES,
        ib[
            [
                "USA_PRES",
                "TOKYO_PRES",
                "CMA_PRES",
                "HKO_PRES",
                "NEWDELHI_PRES",
                "REUNION_PRES",
                "BOM_PRES",
                "NADI_PRES",
                "WELLINGTON_PRES",
            ]
        ].mean(axis=1, skipna=True),
    )
    ib = ib.rename(columns={col: col.lower() for col in ib.columns}).rename(
        columns={
            "usa_sshs": "sshs",
            "sid": "track_id",
            "pres": "slp",
            "iso_time": "time",
        }
    )
    ib.loc[ib.lon < 0, "lon"] += 360
    ib["hemisphere"] = np.where(ib.lat > 0, "N", "S")
    ib["basin"] = (
        ib.basin.replace("EP", "ENP").replace("WP", "WNP").replace("NA", "NATL")
    )
    ib["day"] = ib.time.dt.day
    ib["month"] = ib.time.dt.month
    ib["year"] = ib.time.dt.year
    ib = add_season(ib)
    ib = ib[
        [
            "track_id",
            "time",
            "lon",
            "lat",
            "hemisphere",
            "basin",
            "season",
            "sshs",
            "slp",
            "wind10",
            "year",
            "month",
            "day",
        ]
    ]
    # Save
    ib.to_csv(csv_output)
    with open(pkl_output, "wb") as handle:
        pkl.dump(ib, handle)
    return ib


def load_ibtracs():
    stream = pkg_resources.resource_stream(
        __name__, "_data/ibtracs.since1980.cleaned.csv"
    )
    ib = pd.read_csv(
        stream,
        keep_default_na=False,
        index_col=0,
        na_values=["", " "],
        dtype={"slp": float, "wind10": float, "season": str},
        parse_dates=["time"],
    )
    return ib


def load_TEtracks(
    file="tests/tracks_ERA5.csv",
    NH_seasons=[1980, 2019],
    SH_seasons=[1981, 2019],
    surf_wind_col="wind10",
    slp_col="slp",
):
    """
    Parameters
    ----------
    file (str): csv file from TempestExtremes StitchNodes output
    surf_wind_col (str): Name of the column with the surface wind to output.
    slp_col (str): Name of the column with the sea-level pressure. If None, no sshs computation.

    Returns
    -------
    pd.DataFrame
        Columns as described in the module header
    """
    tracks = pd.read_csv(file)
    tracks = tracks.rename(columns={c: c[1:] for c in tracks.columns[1:]})
    tracks = tracks.rename(columns={surf_wind_col: "wind10", slp_col: "slp"})

    tracks["time"] = get_time(tracks.year, tracks.month, tracks.day, tracks.hour)
    tracks.loc[tracks.lon < 0, "lon"] += 360
    tracks["hemisphere"] = np.where(tracks.lat > 0, "N", "S")
    tracks["basin"] = get_basin(tracks.lon.values, tracks.lat.values)
    tracks = add_season(tracks)
    tracks = tracks[
        ((tracks.season >= NH_seasons[0]) & (tracks.season <= NH_seasons[1]))
        | (tracks.hemisphere == "S")
    ]
    tracks = tracks[
        ((tracks.season >= SH_seasons[0]) & (tracks.season <= SH_seasons[1]))
        | (tracks.hemisphere == "N")
    ]
    tracks[slp_col] /= 100
    if slp_col != None:
        tracks["sshs"] = sshs_from_pres(tracks.slp.values)
    else:
        tracks["sshs"] = np.nan
    return tracks[
        [
            "track_id",
            "time",
            "lon",
            "lat",
            "hemisphere",
            "basin",
            "season",
            "sshs",
            "slp",
            "wind10",
            "year",
            "month",
            "day",
        ]
    ]


_HRMIP_TRACK_data_vars = [
    "vor_tracked",
    "lon2",
    "lat2",
    "vor850",
    "lon3",
    "lat3",
    "vor700",
    "lon4",
    "lat4",
    "vor600",
    "lon5",
    "lat5",
    "vor500",
    "lon6",
    "lat6",
    "vor250",
    "lon7",
    "lat7",
    "wind10",
]

_TRACK_data_vars = [
    "vor_tracked",
    "lon1",
    "lat1",
    "vor850",
    "lon2",
    "lat2",
    "vor700",
    "lon3",
    "lat3",
    "vor600",
    "lon4",
    "lat4",
    "vor500",
    "lon5",
    "lat5",
    "vor400",
    "lon6",
    "lat6",
    "vor300",
    "lon7",
    "lat7",
    "vor200",
    "lon8",
    "lat8",
    "slp",
    "lon9",
    "lat9",
    "wind925",
    "lon10",
    "lat10",
    "wind10",
]


def load_TRACKtracks(
    file="tests/TRACK/19501951.dat",
    origin="HRMIP",
    season=None,
):
    """
    Parameters
    ----------
    file (str): Path to the TRACK output file
    origin (str): 'ERA5' or 'HRMIP'
    season (str): If None, is read from the _data

    Returns
    -------
    pd.DataFrame
        Columns as described in the module header
    """
    if origin == "ERA5":
        data_vars = _TRACK_data_vars
        time_format = "calendar"
    else:
        data_vars = _HRMIP_TRACK_data_vars
        time_format = "time_step"
    f = open(file)
    tracks = pd.DataFrame()
    line0 = f.readline()
    line1 = f.readline()
    line2 = f.readline()
    nb_tracks = int(line2.split()[1])
    c = 0
    track_id = 0
    time_step = []
    lon = []
    lat = []
    data = [[]]
    for line in f:
        if line.startswith("TRACK_ID"):
            data = pd.DataFrame(
                np.array(data), columns=data_vars[: np.shape(np.array(data))[1]]
            )
            tracks = tracks.append(
                pd.DataFrame(
                    {
                        "track_id": [track_id] * len(time_step),
                        "time_step": time_step,
                        "lon": lon,
                        "lat": lat,
                    }
                ).join(data)
            )
            c += 1
            if season == None:
                season = line.split()[-1][:-6]
            track_id = season + "-" + str(c)
            time_step = []
            lon = []
            lat = []
            data = []

        elif line.startswith("POINT_NUM"):
            pass
        else:
            time_step.append(line.split()[0])
            lon.append(float(line.split()[1]))
            lat.append(float(line.split()[2]))
            rest = line.split()[3:]
            mask = np.array(rest) == "&"
            data.append(np.array(rest)[~mask])
    f.close()

    SH = tracks.lat.mean() < 0
    if len(season) == 4:
        start = np.datetime64(season + "-01-01 00:00:00")
    elif len(season) == 8:
        start = np.datetime64(season[:4] + "-07-01 00:00:00")
    if time_format == "calendar":
        tracks["year"] = season[-4:]  # tracks.time_step.str[:4].astype(int)
        tracks["month"] = tracks.time_step.str[-6:-4]  # .astype(int)
        tracks["day"] = tracks.time_step.str[-4:-2]  # .astype(int)
        tracks["hour"] = tracks.time_step.str[-2:]  # .astype(int)
        tracks["time"] = get_time(tracks.year, tracks.month, tracks.day, tracks.hour)
        tracks["delta"] = tracks["time"] - np.datetime64(season[-4:] + "-01-01 00")
        tracks["time"] = tracks["delta"] + start
    elif time_format == "time_step":
        tracks["time"] = [
            start + np.timedelta64(ts * 6, "h") for ts in tracks.time_step.astype(int)
        ]
    else:
        print("Please enter a valid time_format")
    time = pd.DatetimeIndex(tracks.time)
    tracks["year"] = time.year
    tracks["month"] = time.month
    tracks["day"] = time.day
    tracks["hour"] = time.hour
    tracks["hemisphere"] = "S" if SH else "N"
    tracks["season"] = season
    tracks["basin"] = get_basin(tracks.lon, tracks.lat)
    if "vor850" in tracks.columns:
        tracks["vor850"] = tracks.vor850.astype(float)
    if "vor_tracked" in tracks.columns:
        tracks["vor_tracked"] = tracks.vor_tracked.astype(float)
    if "slp" not in tracks.columns:
        tracks["slp"] = np.nan
        tracks["sshs"] = np.nan
    else:
        tracks["slp"] = tracks.slp.astype(float)
        tracks["sshs"] = sshs_from_pres(tracks.slp)
    if "wind10" not in tracks.columns:
        tracks["wind10"] = np.nan
    else:
        tracks["wind10"] = tracks.wind10.astype(float)
    tracks["ACE"] = tracks.wind10 ** 2 * 1e-4
    if "wind925" not in tracks.columns:
        tracks["wind925"] = np.nan
    else:
        tracks["wind925"] = tracks.wind925.astype(float)
    print("")
    return tracks[
        [
            "track_id",
            "time",
            "lon",
            "lat",
            "hemisphere",
            "basin",
            "season",
            "sshs",
            "slp",
            "wind10",
            "ACE",
            "vor_tracked",
            "vor850",
            "wind925",
            "year",
            "month",
            "day",
            "hour",
        ]
    ]


def open_TRACKpkl(
    path="",
    NH_seasons=[1980, 2019],
    SH_seasons=[1981, 2019],
):
    """

    Parameters
    ----------
    path
    NH_seasons
    SH_seasons

    Returns
    -------

    """
    with open(path, "rb") as handle:
        tracks = pkl.load(handle)
    tracks = add_season(tracks)
    tracks = tracks[
        ((tracks.season >= NH_seasons[0]) & (tracks.season <= NH_seasons[1]))
        | (tracks.hemisphere == "S")
    ]
    tracks = tracks[
        ((tracks.season >= SH_seasons[0]) & (tracks.season <= SH_seasons[1]))
        | (tracks.hemisphere == "N")
    ]
    return tracks


def load_CNRMtracks(
    file="tests/tracks_CNRM.csv",
    NH_seasons=[1980, 2019],
    SH_seasons=[1981, 2019],
):
    tracks = pd.read_csv(file)
    tracks = tracks.rename(
        columns={
            "ID": "track_id",
            "Date": "time",
            "Longitude": "lon",
            "Latitude": "lat",
            "Pressure": "slp",
            "Wind": "wind10",
        }
    )
    tracks["hemisphere"] = np.where(tracks.lat > 0, "N", "S")
    tracks["basin"] = get_basin(tracks.lon.values, tracks.lat.values)
    tracks["time"] = tracks.time.astype(np.datetime64)
    tracks["year"] = tracks.time.dt.year
    tracks["month"] = tracks.time.dt.month
    tracks["day"] = tracks.time.dt.day
    tracks = add_season(tracks)
    tracks = tracks[
        ((tracks.season >= NH_seasons[0]) & (tracks.season <= NH_seasons[1]))
        | (tracks.hemisphere == "S")
    ]
    tracks = tracks[
        ((tracks.season >= SH_seasons[0]) & (tracks.season <= SH_seasons[1]))
        | (tracks.hemisphere == "N")
    ]
    tracks["sshs"] = sshs_from_pres(tracks.slp)
    return tracks[
        [
            "track_id",
            "time",
            "lon",
            "lat",
            "hemisphere",
            "basin",
            "season",
            "sshs",
            "slp",
            "wind10",
            "year",
            "month",
            "day",
        ]
    ]


def is_leap(yr):
    if yr % 4 == 0:
        if yr % 100 == 0:
            if yr % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def get_time(year, month, day, hour):
    time = (
        year.astype(str)
        + "-"
        + month.astype(str)
        + "-"
        + day.astype(str)
        + " "
        + hour.astype(str)
        + ":00"
    ).astype(np.datetime64)
    return time


def sshs_from_wind(wind):
    sshs = np.where(wind <= 60 / 3.6, -1, None)
    sshs = np.where((sshs == None) & (wind < 120 / 3.6), 0, sshs)
    sshs = np.where((sshs == None) & (wind < 150 / 3.6), 1, sshs)
    sshs = np.where((sshs == None) & (wind < 180 / 3.6), 2, sshs)
    sshs = np.where((sshs == None) & (wind < 210 / 3.6), 3, sshs)
    sshs = np.where((sshs == None) & (wind < 240 / 3.6), 4, sshs)
    sshs = np.where((sshs == None) & (~np.isnan(wind)), 5, sshs)
    sshs = np.where(sshs == None, np.nan, sshs)
    return sshs


def sshs_from_pres(p):
    sshs = np.where(p > 990, -1, None)
    sshs = np.where((sshs == None) & (p >= 980), 0, sshs)
    sshs = np.where((sshs == None) & (p >= 970), 1, sshs)
    sshs = np.where((sshs == None) & (p >= 965), 2, sshs)
    sshs = np.where((sshs == None) & (p >= 945), 3, sshs)
    sshs = np.where((sshs == None) & (p >= 920), 4, sshs)
    sshs = np.where((sshs == None) & (~np.isnan(p)), 5, sshs)
    sshs = np.where(sshs == None, np.nan, sshs)
    return sshs


# TODO : Optimiser cette fonction
def get_basin(lon, lat):
    basin = []
    for x, y in zip(lon, lat):
        ok = False
        if y >= 0:
            for b in NH:
                if NH[b].contains(Point(x, y)):
                    basin.append(b)
                    ok = True
                    break
        else:
            for b in SH:
                if SH[b].contains(Point(x, y)):
                    basin.append(b)
                    ok = True
                    break
        if ok == False:
            basin.append(np.nan)
    return basin


def get_basin_old(hemisphere, lon, lat):
    basin = np.where((hemisphere == "N") & (lon > 40) & (lon <= 100), "NI", "")
    basin = np.where(
        (hemisphere == "N")
        & (lon > 100)
        & ((lon <= 200) | ((lat >= 35) & (lon <= 250))),
        "WNP",
        basin,
    )
    basin = np.where(
        (hemisphere == "N")
        & (basin != "WNP")
        & (lon > 200)
        & ((lon <= 260) | ((lat <= 15) & (lon <= 290))),
        "ENP",
        basin,
    )
    basin = np.where((hemisphere == "N") & (basin != "ENP") & (lon > 260), "NA", basin)
    basin = np.where((hemisphere == "S") & (lon > 20) & (lon <= 130), "SI", basin)
    basin = np.where((hemisphere == "S") & (lon > 130) & (lon <= 300), "SP", basin)
    basin = np.where((hemisphere == "S") & (basin == ""), "SA", basin)
    return basin


def add_season(tracks):
    if "season" in tracks.columns:
        tracks = tracks.drop(columns="season")
    group = (
        tracks.groupby(["track_id"])[["year", "month"]]
        .mean()
        .astype(int)
        .join(
            tracks[["track_id", "hemisphere"]].drop_duplicates().set_index("track_id"),
            on="track_id",
        )
    )
    hemi, yr, mth = group.hemisphere.values, group.year.values, group.month.values
    season = np.where(hemi == "N", yr, None)
    season = np.where((hemi == "S") & (mth >= 7), yr + 1, season)
    season = np.where((hemi == "S") & (mth <= 6), yr, season)
    # _ = np.where(
    #    (hemi == "S"),
    #    np.core.defchararray.add(season.astype(str), np.array(["-"] * len(season))),
    #    season,
    # ).astype(str)
    # season = np.where(
    #    (hemi == "S"), np.core.defchararray.add(_, (season + 1).astype(str)), season
    # )
    group["season"] = season.astype(int)
    tracks = tracks.join(group[["season"]], on="track_id")
    return tracks


def to_dt(t):
    ts = np.floor((t - np.datetime64("1970-01-01T00:00:00")) / np.timedelta64(1, "s"))
    return np.array(
        [datetime.utcfromtimestamp(t) if not np.isnan(t) else np.nan for t in ts]
    )


def match_tracks(tracks1, tracks2, name1="algo", name2="ib", maxd=8, mindays=1):
    """

    Parameters
    ----------
    tracks1 (pd.DataFrame): First tracks DataFrame
    tracks2 (pd.DataFrame): Second tracks DataFrame
    name1 (str): name to append corresponding to the first df
    name2 (str): name to append corresponding to the second df
    maxd (numeric): Maximum allowed distance between two tracks
    mindays (int): Minimum number of days in common between two tracks

    Returns
    -------
    pd.DataFrame
        with the track ids of the matching trajectories in tracks1 and tracks2
    """
    tracks1, tracks2 = (
        tracks1[["track_id", "lon", "lat", "time"]],
        tracks2[["track_id", "lon", "lat", "time"]],
    )
    merged = pd.merge(tracks1, tracks2, on="time")
    X = np.concatenate([[merged.lat_x], [merged.lon_x]]).T
    Y = np.concatenate([[merged.lat_y], [merged.lon_y]]).T
    merged["dist"] = haversine_vector(X, Y, unit=Unit.DEGREES)
    dist = merged.groupby(["track_id_x", "track_id_y"])[["dist"]].mean()
    temp = (
        merged.groupby(["track_id_x", "track_id_y"])[["dist"]]
        .count()
        .rename(columns={"dist": "temp"})
    )
    matches = dist.join(temp)
    matches = matches[(matches.dist < maxd) & (matches.temp > mindays * 4)]
    matches = (
        matches.loc[matches.groupby("track_id_x")["dist"].idxmin()]
        .reset_index()
        .rename(columns={"track_id_x": "id_" + name1, "track_id_y": "id_" + name2})
    )
    return matches


def match_william(tracks1, tracks2, name1="algo", name2="ib"):
    tracks1, tracks2 = (
        tracks1[["track_id", "lon", "lat", "time"]],
        tracks2[["track_id", "lon", "lat", "time"]],
    )
    merged = pd.merge(tracks1, tracks2, on="time")
    X = np.concatenate([[merged.lat_x], [merged.lon_x]]).T
    Y = np.concatenate([[merged.lat_y], [merged.lon_y]]).T
    merged["dist"] = haversine_vector(X, Y, unit=Unit.KILOMETERS)
    merged = merged[merged.dist <= 300]
    temp = (
        merged.groupby(["track_id_x", "track_id_y"])[["dist"]]
        .count()
        .rename(columns={"dist": "temp"})
    )
    matches = (
        merged[["track_id_x", "track_id_y"]]
        .drop_duplicates()
        .join(temp, on=["track_id_x", "track_id_y"])
    )
    maxs = matches.groupby("track_id_x")[["temp"]].max().reset_index()
    matches = maxs.merge(matches)[["track_id_x", "track_id_y", "temp"]]
    dist = merged.groupby(["track_id_x", "track_id_y"])[["dist"]].mean()
    matches = matches.join(dist, on=["track_id_x", "track_id_y"])
    matches = matches.rename(
        columns={"track_id_x": "id_" + name1, "track_id_y": "id_" + name2}
    )
    return matches


if __name__ == "__main__":
    # t = load_TRACKtracks()
    pass
