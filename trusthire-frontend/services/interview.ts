export const getInterviewQuestions = async (skills: string[]) => {
  const res = await fetch(
    "http://127.0.0.1:8000/api/v1/interview-questions",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(skills),
    }
  );

  return res.json();
};