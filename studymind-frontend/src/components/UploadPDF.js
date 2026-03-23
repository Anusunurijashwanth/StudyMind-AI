import { useState } from "react";
import { uploadPDF } from "../services/api";

export default function UploadPDF() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const upload = async () => {
    if (!file) {
      alert("Select PDF first");
      return;
    }

    try {
      setStatus("Uploading...");

      const formData = new FormData();
      formData.append("file", file);

      const data = await uploadPDF(formData);
      setStatus(data.status);
    } catch (error) {
      console.error(error);
      setStatus("Upload failed");
    }
  };

  return (
    <div className="upload-box">
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button className="upload-btn" onClick={upload}>
        Upload PDF
      </button>
      {status && <p>{status}</p>}
    </div>
  );
}