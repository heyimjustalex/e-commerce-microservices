// Script for creating init products in mongoDB

db = db.getSiblingDB("shop");

db.createCollection("orders");

db.orders.insertMany([
  {
    _id: ObjectId("10fefe4a1cad4140785928a4"),
    client: "aaa@aaa.com",
    status: "PENDING",
    products: [
      {
        name: "cutlery",
        price: 5.99,
        quantity: 4,
      },
      {
        name: "chair",
        price: 29.99,
        quantity: 2,
      },
    ],
  },
  {
    _id: ObjectId("11fgfe4a1cad4140785928a5"),
    client: "bbb@bbb.com",
    status: "ORDERED",
    products: [
      {
        name: "laptop",
        description: "A powerful computing device",
        price: 1299.99,
        quantity: 1,
      },
    ],
  },
  {
    _id: ObjectId("12fgfe4a1cad4140785928a6"),
    client: "ccc@ccc.com",
    products: [
      {
        name: "headphones",
        description: "Wireless noise-cancelling headphones",
        price: 99.99,
      },
    ],
  },
]);
