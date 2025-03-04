const person = {
    name: "YYY",
    greet: function (message) {
      console.log(`${message}, my name is ${this.name}`);
    },
  };
  
  const anotherPerson = { name: "Yash" };
  
  person.greet.call(person, "Hello");
  person.greet.apply(anotherPerson, ["Hi"]);
  
  const boundGreet = person.greet.bind(anotherPerson);
  boundGreet("Hey");
  