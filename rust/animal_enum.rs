pub enum Animal {
    Dog(String),  // tuple-like, unnamed field
    Cat(String),
    Pig(String),
}

impl Animal {
    pub fn speak(&self) {
        match self {
            Animal::Dog(name) => println!("I'm {} Dog. I say WOOF!", name),
            Animal::Cat(name) => println!("I'm {} Cat. I say MEOW!", name),
            Animal::Pig(name) => println!("I'm {} Pig. I say OINK!", name),
        }
    }
}

fn main() {
    let v = vec![Animal::Dog(String::from("Danny")),
                 Animal::Cat(String::from("Candy")),
                 Animal::Pig(String::from("Peppa"))];
    for a in v {
        a.speak();
    }
}
