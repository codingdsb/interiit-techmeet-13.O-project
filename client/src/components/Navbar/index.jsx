import "./styles.css";

const Navbar = ({setAboutUsPage}) => {
  return (
    <nav>
      <div id='logo'>AirCargo</div>
      <div id='team'>
        Created with ❤️ by <span onClick={() => setAboutUsPage(true)}>Team CodeCargo</span>
      </div>
    </nav>
  );
};

export default Navbar;
