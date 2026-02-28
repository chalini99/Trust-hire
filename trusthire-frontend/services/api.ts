export const verifyResume = async (file: File, github: string) => {
  const formData = new FormData();
  formData.append("resume", file);
  formData.append("github_username", github);

  const res = await fetch("http://127.0.0.1:8000/api/v1/verify", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Verification failed");
  }

  return res.json();
};