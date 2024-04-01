db = db.getSiblingDB("shop");

db.createCollection("orders");
db.createCollection("products");

db.orders.insertMany([
  {
    _id: ObjectId("71fefe4a1cad4140785928a4"),
    client_email: "aaa@aaa.com",
    status: "PENDING",
    cost: 83.94,
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
    _id: ObjectId("72fefe4a1cad4140785928a4"),
    client_email: "bbb@bbb.com",
    status: "ORDERED",
    cost: 1299.99,
    products: [
      {
        name: "laptop",
        price: 1299.99,
        quantity: 1,
      },
    ],
  },
  {
    _id: ObjectId("73fefe4a1cad4140785928a4"),
    client_email: "ccc@ccc.com",
    status: "PENDING",
    cost: 699.93,
    products: [
      {
        name: "headphones",
        price: 99.99,
        quantity: 7,
      },
    ],
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
