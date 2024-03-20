// Script for creating init users in mongoDB

db = db.getSiblingDB("shop");

db.createCollection("users");

db.users.insertMany([
  {
    email: "aaa@aaa.com",
    password_hash:
      "9c520caf74cff9b9a891be3694b20b3586ceb17f2891ceb1d098709c1e0969a3",
  },
  {
    email: "bbb@bbb.com",
    password_hash:
      "77cd27bc3de668c18ed6be5f5c2909ffdacdf67705c30d132003ad5a89085deb",
  },
  {
    email: "ccc@ccc.com",
    password_hash:
      "7ff5e3dac2a290dd7b14f69f1b435be64003aabe2cd98acaa5490f0e3d1483f3",
  },
]);
