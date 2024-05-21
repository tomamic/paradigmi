pub trait Animal {
    fn speak(&self);
}

pub struct Dog {
    name: String
}
impl Dog {
    pub fn new(name: &str) -> Dog {
        Dog{ name: name.to_string() }
    }
}
impl Animal for Dog {
    fn speak(&self) {
        println!("I'm {} Dog. I say WOOF!", self.name);
    }
}

pub struct Cat {
    name: String
}
impl Cat {
    pub fn new(name: &str) -> Cat {
        Cat{ name: name.to_string() }
    }
}
impl Animal for Cat {
    fn speak(&self) {
        println!("I'm {} Cat. I say MEOW!", self.name);
    }
}

pub struct Pig {
    name: String
}
impl Pig {
    pub fn new(name: &str) -> Pig {
        Pig{ name: name.to_string() }
    }
}
impl Animal for Pig {
    fn speak(&self) {
        println!("I'm {} Pig. I say OINK!", self.name);
    }
}


