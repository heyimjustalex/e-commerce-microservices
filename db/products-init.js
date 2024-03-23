// Script for creating init products in mongoDB

db = db.getSiblingDB("shop");

db.createCollection("products");
db.createCollection("categories");
db.categories.insertMany([
  {
    _id: ObjectId("21fefe4a1cad4140785928a4"),
    name: "Electronics",
  },
  {
    _id: ObjectId("22fefe4a1cad4140785928a4"),
    name: "Kitchen",
  },
  {
    _id: ObjectId("23fefe4a1cad4140785928a4"),
    name: "Furniture",
  },
]);
db.products.insertMany([
  {
    _id: ObjectId("10fefe4a1cad4140785928a4"),
    name: "Cuterly",
    description: "An interesting set of cuterly",
    price: 5.99,
    categories: [ObjectId("22fefe4a1cad4140785928a4")],
  },
  {
    _id: ObjectId("11fefe4a1cad4140785928a4"),
    name: "Chair",
    description: "A comfortable armchair",
    price: 29.99,
    categories: [
      ObjectId("23fefe4a1cad4140785928a4"),
      ObjectId("22fefe4a1cad4140785928a4"),
    ],
  },
  {
    _id: ObjectId("12fefe4a1cad4140785928a4"),
    name: "Laptop",
    description: "A powerful computing device",
    price: 1299.99,
    categories: [ObjectId("21fefe4a1cad4140785928a4")],
  },
  {
    _id: ObjectId("13fefe4a1cad4140785928a4"),
    name: "Headphones",
    description: "Wireless noise-cancelling headphones",
    price: 99.99,
    categories: [ObjectId("21fefe4a1cad4140785928a4")],
  },
]);
