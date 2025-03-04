// //Lexical scoping
// function init(){
//     var name = "yash";
//     function displayName(){
//         console.log(name);
//     }
//     displayName()
// }
// init()

// //Scoping with let and const
// if (Math.random() > 0.5){
//     var x = 1;
// } else {
//     var x = 2;
// }
// console.log(x); 

//closures
function counter() {
    let count = 0;
    return function () {
      count++;
      console.log(count);
    };
  }
  
  const increment = counter();
  increment();
  increment();
  increment();
  increment();