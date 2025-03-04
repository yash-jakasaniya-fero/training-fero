function Animal(name) {
    this.name = name;
  }
  
  Animal.prototype.speak = function () {
    console.log(`${this.name} makes a noise.`);
  };
  
  const dog = new Animal("Dog");
  dog.speak();  