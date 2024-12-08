function displayDate() {
    const today = new Date();
    const date = today.toDateString();
    const time = today.toLocaleTimeString();
    document.getElementById('currentDate').innerHTML = `${date} ${time}`;
  }

document.addEventListener('DOMContentLoaded', (event) => {
  // Call displayDate function immediately upon page load
  displayDate();
});