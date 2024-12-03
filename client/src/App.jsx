import { useState } from "react";
import OutputPage from "./pages/OutputPage";
import InputPage from "./pages/InputPage";
import Navbar from "./components/Navbar";
import AboutUsPage from "./pages/AboutUsPage";

const App = () => {
  const [result, setResult] = useState(null);
  const [aboutUsPage, setAboutUsPage] = useState(false);
  return (
    <>
      <Navbar setAboutUsPage={setAboutUsPage} />
      {aboutUsPage ? (
        <AboutUsPage setAboutUsPage={setAboutUsPage} />
      ) : result ? (
        <OutputPage result={result} setResult={setResult} />
      ) : (
        <InputPage setResult={setResult} result={result} />
      )}
    </>
  );
};

export default App;
