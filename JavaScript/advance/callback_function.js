function greet(name) {
    console.log(`Hello, ${name}!`);
}

function executeCallback(callback, arg) {
    console.log("Executing callback...");
    callback(arg);
}

executeCallback(greet, "Yash");
