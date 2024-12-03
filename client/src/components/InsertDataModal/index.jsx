import { useState } from "react";
import "./styles.css";
import InputBox from "../InputBox";
import { getPackages, getULDs } from "./csvToJson";
const InsertDataModal = ({
  packages,
  ulds,
  setPackages,
  setUlds,
  isOpen,
  setModalOpen,
}) => {
  const [packageCSV, setPackageCSV] = useState("");
  const [uldCSV, setUldCSV] = useState("");
  const [error, setError] = useState("");

  const insertData = () => {
    setError("");
    if (uldCSV) {
      try {
        const newUlds = getULDs(uldCSV);
        setUlds([...ulds, ...newUlds]);
      } catch (err) {
        console.log(err);
        setError("Something is wrong in CSV data of ULDs, please check.");
        return;
      }
    }
    if (packageCSV) {
      try {
        if (uldCSV) {
          setUldCSV("");
        }
        const newPackages = getPackages(packageCSV);
        setPackages([...packages, ...newPackages]);
      } catch (err) {
        setError("Something is wrong in CSV data of Packages, please check.");
        return;
      }
    }

    if (uldCSV || packageCSV) {
      setUldCSV("");
      setPackageCSV("");
      setModalOpen(false);
    } else {
      setError("Please fill at least one CSV");
    }
  };

  return (
    <div className={`overlay ${isOpen ? "active" : ""}`}>
      <div className='modalBody'>
        <div className='modalHeader'>
          <h1>Insert Data</h1>
          <button onClick={() => setModalOpen(false)}>Close</button>
        </div>

        {/* error message */}
        <div className='error'>{error}</div>

        {/* modal content */}
        <div className='modalContent'>
          {/* ULD CSV BOX */}
          <div>
            <label>
              CSV for ULDs (Sequence: name, length, width, height, max weight)
            </label>
            <InputBox
              type={"textarea"}
              label={"Enter CSV for ULDs (Do not include the headings)"}
              value={uldCSV}
              setValue={setUldCSV}
            />
          </div>

          {/* Package CSV BOX */}
          <div>
            <label>
              CSV for Packages (Sequence: name, length, width, height, weight,
              type (Priority or Economy), delay cost)
            </label>
            <InputBox
              type={"textarea"}
              label={"Enter CSV for Packages (Do not include the headings)"}
              value={packageCSV}
              setValue={setPackageCSV}
            />
          </div>
        </div>

        <button onClick={insertData}>Insert Data</button>
      </div>
    </div>
  );
};

export default InsertDataModal;
