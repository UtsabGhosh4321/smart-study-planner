const StatsCard = ({ title, value }) => {
  return (
    <div className="bg-blue-500 text-white p-4 rounded-lg shadow">
      <h3 className="text-lg">{title}</h3>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
};

export default StatsCard;