// Script for creating init products in mongoDB

db = db.getSiblingDB("shop");

db.createCollection("products");
db.createCollection("categories");
db.createCollection("orders");

db.categories.insertMany([
  {
    _id: ObjectId("21fefe4a1cad4140785928a4"),
    name: "electronics",
  },
  {
    _id: ObjectId("22fefe4a1cad4140785928a4"),
    name: "kitchen",
  },
  {
    _id: ObjectId("23fefe4a1cad4140785928a4"),
    name: "furniture",
  },
]);

db.products.insertMany([
  {
    _id: ObjectId("10fefe4a1cad4140785928a4"),
    name: "cutlery",
    description: "An interesting set of cutlery",
    price: 5.99,
    quantity: 200,
    categories: [ObjectId("22fefe4a1cad4140785928a4")],
  },
  {
    _id: ObjectId("11fefe4a1cad4140785928a4"),
    name: "chair",
    description: "A comfortable armchair",
    price: 29.99,
    quantity: 30,
    categories: [
      ObjectId("23fefe4a1cad4140785928a4"),
      ObjectId("22fefe4a1cad4140785928a4"),
    ],
  },
  {
    _id: ObjectId("12fefe4a1cad4140785928a4"),
    name: "laptop",
    description: "A powerful computing device",
    price: 1299.99,
    quantity: 1,
    categories: [ObjectId("21fefe4a1cad4140785928a4")],
  },
  {
    _id: ObjectId("13fefe4a1cad4140785928a4"),
    name: "headphones",
    description: "Wireless noise-cancelling headphones",
    price: 99.99,
    quantity: 1,
    categories: [ObjectId("21fefe4a1cad4140785928a4")],
  },
]);

db.orders.insertMany([
  {
    _id: ObjectId("71fefe4a1cad4140785928a4"),
    status: "ACCEPTED",
  },
  {
    _id: ObjectId("72fefe4a1cad4140785928a4"),
    status: "ACCEPTED",
  },
  {
    _id: ObjectId("73fefe4a1cad4140785928a4"),
    status: "REJECTED",
  },
]);
