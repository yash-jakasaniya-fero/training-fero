setTimeout(() => console.log("Executed after 2 seconds"), 2000);

let count = 0;
const interval = setInterval(() => {
  count++;
  console.log("Interval running:", count);
  if (count === 5) clearInterval(interval);
}, 1000);
