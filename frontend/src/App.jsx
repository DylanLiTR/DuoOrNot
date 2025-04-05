import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [imageURL, setImageURL] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const uploaded = e.target.files[0];
    if (uploaded) {
      setFile(uploaded);
      setImageURL(URL.createObjectURL(uploaded));
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("image", file);

    setLoading(true);
    const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Duo or Not?</h1>

      <input type="file" accept="image/*" onChange={handleFileChange} />

      <br /><br />

      {imageURL && (
        <img
          src={imageURL}
          alt="Uploaded preview"
          className="preview-img"
        />
      )}

      <br />

      <button onClick={handleUpload} disabled={!file || loading} className={result ? result.prediction === "duolingo" ? "positive" : "negative" : ""}>
        {result ? (result.prediction === "duolingo" ? "Duo!" : "Not Duo") : (loading ? "Detecting..." : "Check")}
      </button>

      {/* {result && (
        <div className="result">
          <h2 className={result.prediction === "duolingo" ? "positive" : "negative"}>
            {result.prediction === "duolingo" ? "✅ Duo" : "❌ Not Duo"}
          </h2>
        </div>
      )} */}
    </div>
  );
}

export default App;
