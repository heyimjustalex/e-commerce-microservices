// Script for creating init products in mongoDB

db = db.getSiblingDB("shop");

db.createCollection("products");

db.products.insertMany([
  [
    {
      name: "Book",
      description: "An interesting novel",
      price: 5.99,
    },
    {
      name: "Chair",
      description: "A comfortable armchair",
      price: 29.99,
    },
    {
      name: "Laptop",
      description: "A powerful computing device",
      price: 1299.99,
    },
    {
      name: "Headphones",
      description: "Wireless noise-cancelling headphones",
      price: 99.99,
    },
  ],
]);
