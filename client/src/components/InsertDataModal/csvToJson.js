export const getULDs = (csv) => {
  const rows = csv.split(/\n+/).filter((row) => row !== "");

  let uldData;
  const ulds = rows.map((row) => {
    uldData = row.split(",");

    if (uldData.length !== 5) {
      throw new Error("Something is wrong in CSV data of ULDs, please check.");
    }

    return {
      name: uldData[0],
      length: parseFloat(uldData[1]),
      width: parseFloat(uldData[2]),
      height: parseFloat(uldData[3]),
      maxWeight: parseFloat(uldData[4]),
    };
  });

  return ulds;
};

export const getPackages = (csv) => {
  const rows = csv.split(/\n+/).filter((row) => row !== "");
  let packageData;
  const packages = rows.map((row) => {
    packageData = row.split(",");

    if (packageData.length !== 7) {
      throw new Error(
        "Something is wrong in CSV data of Packages, please check."
      );
    }
    return {
      name: packageData[0],
      length: parseFloat(packageData[1]),
      width: parseFloat(packageData[2]),
      height: parseFloat(packageData[3]),
      weight: parseFloat(packageData[4]),
      isPriority: packageData[5].toLowerCase() == "priority",
      delayCost: parseFloat(packageData[6]),
    };
  });

  return packages;
};
