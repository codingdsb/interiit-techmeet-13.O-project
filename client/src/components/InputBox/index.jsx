import "./styles.css";

const InputBox = ({ label, type, value, setValue, boxWidth, boxHeight }) => {
  return (
    <>
      {type == "textarea" ? (
        <div className='inputBox'>
          <textarea
            placeholder={label}
            value={value}
            onChange={(e) => setValue(e.target.value)}
          ></textarea>
        </div>
      ) : (
        <div className='inputBox'>
          <input
            type={type}
            placeholder={label}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            style={{ width: boxWidth, height: boxHeight }}
            min={0}
          />
        </div>
      )}
    </>
  );
};

export default InputBox;