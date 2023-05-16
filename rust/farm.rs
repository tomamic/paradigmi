pub mod animal;
use crate::animal::*;

pub struct Farm<T: Animal> {
    animals: Vec<T>
}
impl<T: Animal> Farm<T> {
    fn run(&self) {
        for a in self.animals.iter() {
            a.say();
        }
    }
}

pub struct DynFarm {
    pub animals: Vec<Box<dyn Animal>>
}
impl DynFarm {
    pub fn run(&self) {
        for a in self.animals.iter() {
            a.say();
        }
    }
}

fn main() {
    // trait bound -- solved by compiler to a concrete type
    // all objects must be of the same type
    let farm = Farm{ animals: vec![
        Pig::new("Peppa"),
        Pig::new("George")
    ]};
    farm.run();

    // boxed trait objects -- runtime polymorphism
    // dynamic dispatch
    let dynfarm = DynFarm{ animals: vec![
        Box::new(Dog::new("Danny")),
        Box::new(Cat::new("Candy")),
        Box::new(Pig::new("Peppa")),
        Box::new(Pig::new("George"))
    ]};
    dynfarm.run()
}
