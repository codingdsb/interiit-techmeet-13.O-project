import { useState } from "react";
import "./styles.css";

const OutputPage = ({ result, setResult }) => {
  const [showPlacedPackages, setShowPlacedPackages] = useState(true);
  const [showUnplacedPackages, setShowUnplacedPackages] = useState(true);

  const getFile = () => {
    fetch("http://localhost:5000/get-file", {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
        "Access-Control-Allow-Origin": "http://localhost:5000",
      },
      body: JSON.stringify({
        output_data: result.data,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        window.location.href =
          "http://localhost:5000/download-file/" + data.filename;
      })
      .catch((err) => console.log(err));
  };

  return (
    <>
      <button onClick={() => setResult(null)}>
        Clear Result And Go To Input Page
      </button>

      {result.success ? (
        <div id='outputpageContent'>
          <div className='tag'>Total Cost: {result.data.total_cost}</div>
          <div className='tag'>
            Number of Packages Placed: {result.data.packages_placed}
          </div>
          <div className='tag'>
            Number of ULDs containing priority packages:{" "}
            {result.data.priority_uld_count}
          </div>
          <button id="downloadbtn" onClick={getFile}>Download Output in TXT File</button>
          <div id='checks'>
            <span>
              <input
                type='checkbox'
                checked={showPlacedPackages}
                onChange={(e) => setShowPlacedPackages(e.target.checked)}
              />{" "}
              Show Placed Packages
            </span>
            <span>
              <input
                type='checkbox'
                checked={showUnplacedPackages}
                onChange={(e) => setShowUnplacedPackages(e.target.checked)}
              />{" "}
              Show Unplaced Packages
            </span>
          </div>
          <table>
            <thead>
              <tr>
                <th>Sr No.</th>
                <th>Package Name</th>
                <th>Type</th>
                <th>ULD Containing The Package</th>
                <th>Coordinates of Reference Corner</th>
                <th>
                  Coordinates of Corner Diagonally Opposite to Reference Corner
                </th>
              </tr>
            </thead>
            <tbody>
              {result.data.packages.map((pkg, idx) => {
                let pkgPlaced = pkg.uld;
                if (
                  (pkgPlaced && showPlacedPackages) ||
                  (!pkgPlaced && showUnplacedPackages)
                ) {
                  return (
                    <tr key={idx}>
                      <td>{idx + 1}</td>
                      <td>{pkg.name}</td>
                      <td>{pkg.is_priority ? "Priority" : "Economy"}</td>
                      <td>{pkg.uld ? pkg.uld : "None"}</td>
                      <td>
                        {pkg.reference_corner
                          ? pkg.reference_corner
                          : "(-1,-1,-1)"}
                      </td>
                      <td>
                        {pkg.diagonally_opposite_corner
                          ? pkg.diagonally_opposite_corner
                          : "(-1,-1,-1)"}
                      </td>
                    </tr>
                  );
                }
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <div className='error'>
          Something went wrong, please check if you provided all the input
          fields correctly
        </div>
      )}
    </>
  );
};

export default OutputPage;
