import InputBox from "../../components/InputBox";
import { useState } from "react";
import "./styles.css";
import InsertDataModal from "../../components/InsertDataModal";

const InputPage = ({ result, setResult }) => {
  const inputBoxWidth = "100%";

  // cost for ULD for priority packages
  const [k, setK] = useState(0);

  // insert modal data state
  const [modalOpen, setModalOpen] = useState(false);

  // loading and error state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // ULD form data
  const [uldName, setUldName] = useState("");
  const [uldLength, setUldLength] = useState(0);
  const [uldWidth, setUldWidth] = useState(0);
  const [uldHeight, setUldHeight] = useState(0);
  const [uldMaxWeight, setUldMaxWeight] = useState(0);
  const [ulds, setUlds] = useState([]);

  // Package Form Data
  const [packageName, setPackageName] = useState("");
  const [packageLength, setPackageLength] = useState(0);
  const [packageWidth, setPackageWidth] = useState(0);
  const [packageHeight, setPackageHeight] = useState(0);
  const [packageWeight, setPackageWeight] = useState(0);
  const [packageIsPriority, setPackageIsPriority] = useState("Priority");
  const [packageDelayCost, setPackageDelayCost] = useState(0);
  const [packages, setPackages] = useState([]);

  // get result function

  const getResult = () => {
    setLoading(true);
    const reqBody = {
      priority_uld_cost: parseFloat(k),
      ulds,
      packages,
    };

    fetch("http://localhost:5000/get-coords", {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
        "Access-Control-Allow-Origin": "http://localhost:5000",
      },
      body: JSON.stringify(reqBody),
    })
      .then((res) => {
        return res.json();
      })
      .then((data) =>{
        setResult(data);
        setLoading(false);
      })
      .catch((err) =>  {
        setError(err);
        setLoading(false);
      });
  };

  return (
    <div className='inputPage'>
      <InsertDataModal
        isOpen={modalOpen}
        packages={packages}
        setPackages={setPackages}
        ulds={ulds}
        setUlds={setUlds}
        setModalOpen={setModalOpen}
      />
      <div className='headContent'>
        <label>Cost of each ULD containing a priority package</label>
        <InputBox
          label={"Cost of each ULD containing a priority package"}
          type={"number"}
          value={k}
          setValue={setK}
          boxWidth={"50%"}
          boxHeight={"2.5rem"}
        />

        <button onClick={getResult}>{
            loading ? "Loading..." : "Get Result"
          }</button>
        <button onClick={() => setModalOpen(true)}>
          Insert Data Using CSV
        </button>
      </div>

      <section>
        <h2>ULDs</h2>

        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Length (cm)</th>
              <th>Width (cm)</th>
              <th>Height (cm)</th>
              <th>Weight Limit (kg)</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <InputBox
                  label={"Name"}
                  type={"text"}
                  value={uldName}
                  setValue={setUldName}
                  boxWidth={inputBoxWidth}
                  boxHeight={"2.5rem"}
                />
              </td>
              <td>
                <InputBox
                  label={"Length"}
                  type={"number"}
                  value={uldLength}
                  setValue={setUldLength}
                  boxWidth={inputBoxWidth}
                  boxHeight={"2.5rem"}
                />
              </td>
              <td>
                <InputBox
                  label={"Width"}
                  type={"number"}
                  value={uldWidth}
                  setValue={setUldWidth}
                  boxWidth={inputBoxWidth}
                  boxHeight={"2.5rem"}
                />
              </td>
              <td>
                <InputBox
                  label={"Height"}
                  type={"number"}
                  value={uldHeight}
                  setValue={setUldHeight}
                  boxWidth={inputBoxWidth}
                  boxHeight={"2.5rem"}
                />
              </td>
              <td>
                <InputBox
                  label={"Max Weight"}
                  type={"number"}
                  value={uldMaxWeight}
                  setValue={setUldMaxWeight}
                  boxWidth={inputBoxWidth}
                  boxHeight={"2.5rem"}
                />
              </td>
              <td>
                <button
                  onClick={() => {
                    if (
                      uldName &&
                      uldLength &&
                      uldWidth &&
                      uldHeight &&
                      uldMaxWeight
                    ) {
                      setUlds([
                        ...ulds,
                        {
                          name: uldName,
                          length: parseFloat(uldLength),
                          width: parseFloat(uldWidth),
                          height: parseFloat(uldHeight),
                          maxWeight: parseFloat(uldMaxWeight),
                        },
                      ]);
                      setUldName("");
                      setUldLength(0);
                      setUldWidth(0);
                      setUldHeight(0);
                      setUldMaxWeight(0);
                    }
                  }}
                >
                  Add
                </button>
              </td>
            </tr>
            {ulds.map((uld) => (
              <tr key={uld.name}>
                <td>{uld.name}</td>
                <td>{uld.length}</td>
                <td>{uld.width}</td>
                <td>{uld.height}</td>
                <td>{uld.maxWeight}</td>
                <td>
                  <button
                    onClick={() =>
                      setUlds(ulds.filter((u) => u.name !== uld.name))
                    }
                  >
                    Remove
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h2>Packages</h2>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Length (cm)</th>
              <th>Width (cm)</th>
              <th>Height (cm)</th>
              <th>Weight (kg)</th>
              <th>Type (Priority/Economy)</th>
              <th>Delay Cost</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <InputBox
                  label={"Name"}
                  type={"text"}
                  value={packageName}
                  setValue={setPackageName}
                  boxWidth={inputBoxWidth}
                  boxHeight={"2.5rem"}
                />
              </td>
              <td>
                <InputBox
                  label={"Length"}
                  type={"number"}
                  value={packageLength}
                  setValue={setPackageLength}
                  boxWidth={inputBoxWidth}
                  boxHeight={"2.5rem"}
                />
              </td>
              <td>
                <InputBox
                  label={"Width"}
                  type={"number"}
                  value={packageWidth}
                  setValue={setPackageWidth}
                  boxWidth={inputBoxWidth}
                  boxHeight={"2.5rem"}
                />
              </td>
              <td>
                <InputBox
                  label={"Height"}
                  type={"number"}
                  value={packageHeight}
                  setValue={setPackageHeight}
                  boxWidth={inputBoxWidth}
                  boxHeight={"2.5rem"}
                />
              </td>
              <td>
                <InputBox
                  label={"Weight"}
                  type={"number"}
                  value={packageWeight}
                  setValue={setPackageWeight}
                  boxWidth={inputBoxWidth}
                  boxHeight={"2.5rem"}
                />
              </td>
              <td>
                <select
                  value={packageIsPriority}
                  onChange={(e) => setPackageIsPriority(e.target.value)}
                >
                  <option value={true}>Priority</option>
                  <option value={false}>Economy</option>
                </select>
              </td>
              <td>
                <InputBox
                  label={"Delay Cost"}
                  type={"number"}
                  value={packageDelayCost}
                  setValue={setPackageDelayCost}
                  boxWidth={inputBoxWidth}
                  boxHeight={"2.5rem"}
                />
              </td>
              <td>
                <button
                  onClick={() => {
                    if (
                      packageName &&
                      packageLength &&
                      packageWidth &&
                      packageHeight &&
                      packageWeight &&
                      packageIsPriority &&
                      (packageIsPriority === "Priority" || packageDelayCost)
                    ) {
                      setPackages([
                        ...packages,
                        {
                          name: packageName,
                          length: parseFloat(packageLength),
                          width: parseFloat(packageWidth),
                          height: parseFloat(packageHeight),
                          weight: parseFloat(packageWeight),
                          isPriority: true
                            ? packageIsPriority === "Priority"
                            : false,
                          delayCost:
                            packageIsPriority === "Priority"
                              ? 0
                              : parseFloat(packageDelayCost),
                        },
                      ]);
                      setPackageName("");
                      setPackageLength(0);
                      setPackageWidth(0);
                      setPackageHeight(0);
                      setPackageWeight(0);
                      setPackageIsPriority("Priority");
                      setPackageDelayCost(0);
                    }
                  }}
                >
                  Add
                </button>
              </td>
            </tr>
            {packages.map((pack) => (
              <tr key={pack.name}>
                <td>{pack.name}</td>
                <td>{pack.length}</td>
                <td>{pack.width}</td>
                <td>{pack.height}</td>
                <td>{pack.weight}</td>
                <td>{pack.isPriority ? "Priority" : "Economy"}</td>
                <td>{pack.delayCost}</td>
                <td>
                  <button
                    onClick={() =>
                      setPackages(packages.filter((p) => p.name !== pack.name))
                    }
                  >
                    Remove
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
};

export default InputPage;
