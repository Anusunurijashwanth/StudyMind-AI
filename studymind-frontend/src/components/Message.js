export default function Message({ msg }) {
  return (
    <div className={`message-row ${msg.type}`}>
      <div className={`message-bubble ${msg.type}`}>
        {msg.text}
      </div>
    </div>
  );
}