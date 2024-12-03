import TeamMemberCard from "../../components/TeamMemberCard";
import "./styles.css";

const AboutUsPage = ({setAboutUsPage}) => {
  const members = [
    {
      name: "Darshan Sunil Bajeja",
      imageUrl: "/darshan-bajeja.png",
      department: "Mathematics and Computing",
      linkedIn: "https://www.linkedin.com/in/darshan-bajeja-158331217/",
      githubUsername: "codingdsb",
      githubLink: "https://github.com/codingdsb",
    },

    {
      name: "Samay Patel",
      imageUrl: "/samay-patel.png",
      department: "Computer Science and Engineering",
      linkedIn: "https://www.linkedin.com/in/samay-patel-321830326/",
      githubUsername: "samay90",
      githubLink: "https://github.com/samay90",
    },

    {
      name: "Dagle Amruta Namdev",
      imageUrl: "amruta-dagle.png",
      department: "Computer Science and Engineering",
      linkedIn: "https://www.linkedin.com/in/amruta-dagle-22b326332/",
      githubUsername: "DagleAmruta15",
      githubLink: "https://github.com/DagleAmruta15",
    },

    {
      name: "Anuneet Gupta",
      imageUrl: "anuneet-gupta.png",
      department: "Mechanical Engineering",
      linkedIn: "https://www.linkedin.com/in/anuneet-gupta-436990310/",
      githubUsername: "anuneet1610",
      githubLink: "https://github.com/anuneet1610",
    },

    {
      name: "Shaurya Sinha",
      imageUrl: "shaurya-sinha.png",
      department: "Computer Science and Engineering",
      linkedIn: "https://www.linkedin.com/in/shaurya-sinha-640695338/",
      githubUsername: "Shaurya-64",
      githubLink: "https://github.com/Shaurya-64",
    },

    {
      name: "Shivam Nishant Rajan",
      imageUrl: "shivam-rajan.png",
      department: "Electrical Engineering",
      linkedIn: "https://www.linkedin.com/in/shivam-rajan-68238b31a/",
      githubUsername: "shivam45783",
      githubLink: "https://github.com/shivam45783",
    },
  ];

  return (
    <div className='aboutUsPage'>
      <button onClick={() => setAboutUsPage(false)}>
        Back
      </button>
      <h1>Team CodeCargo</h1>
      <h2>Who we are?</h2>
      <p>
        We are a team of 6 students from the Indian Institute of Technology
        (IIT). We are coding enthusiasts and
        love building products like these. This product is made as a solution to
        one of the problem statements of the Inter-IIT Tech Meet 13.O of 2024
        organized by the Indian Institute of Technology, Bombay.{" "}
      </p>
      <h2>Meet Our Team</h2>
      <div className='team'>
        {members.map((member) => (
          <TeamMemberCard
            key={member.name}
            name={member.name}
            imageUrl={member.imageUrl}
            department={member.department}
            linkedIn={member.linkedIn}
            githubUsername={member.githubUsername}
            githubLink={member.githubLink}
          />
        ))}
      </div>
    </div>
  );
};

export default AboutUsPage;
