import "./styles.css";

const TeamMemberCard = ({
  name,
  imageUrl,
  department,
  linkedIn,
  githubUsername,
  githubLink,
}) => {
  return (
    <div className='teamMemberCard'>
      <img src={"/images/" + imageUrl} alt={name} />
      <span className='name'>{name}</span>
      <span className="department">BTech in {department} 2024-2028</span>
      <div className="socials">
        <a href={linkedIn} target="_blank">
          <img src='/linkedin.svg' />
          Linked In
        </a>
        <a href={githubLink} target="_blank">
          <img src='/github.svg' />
          @{githubUsername}
        </a>
      </div>
    </div>
  );
};

export default TeamMemberCard;
