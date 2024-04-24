let BACKEND_ADDRESS = import.meta.env.VITE_APP_BACKEND_ADDRESS;

if (!BACKEND_ADDRESS) {
  BACKEND_ADDRESS = "http://invalid-build-arg-VITE_APP_BACKEND_ADDRESS/api";
}

export async function login(loginData) {
  const response = await fetch(`${BACKEND_ADDRESS}/login`, {
    method: "POST",
    body: JSON.stringify(loginData),
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    if (response.status >= 200 && response.status < 500) {
      const res = await response.json();
      const detail = res["detail"];
      throw new Error(detail);
    }
    throw new Error("Service unavaliable!");
  }

  try {
    const data = await response.json();
    return data;
  } catch {
    throw new Error("Login failed");
  }
}

export async function register(registerData) {
  const response = await fetch(`${BACKEND_ADDRESS}/register`, {
    method: "POST",
    body: JSON.stringify(registerData),
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    if (response.status >= 200 && response.status < 500) {
      const res = await response.json();
      const detail = res["detail"];
      throw new Error(detail);
    }
    throw new Error("Service unavaliable!");
  }

  try {
    const data = await response.json();
    return data;
  } catch {
    throw new Error("Register failed");
  }
}

export async function getProducts() {
  console.log("products", BACKEND_ADDRESS);
  const response = await fetch(`${BACKEND_ADDRESS}/products`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    if (response.status >= 200 && response.status < 500) {
      const res = await response.json();
      const detail = res["detail"];
      throw new Error(detail);
    }
    throw new Error("Service unavaliable!");
  }

  var contentType = response.headers.get("content-type");
  if (contentType && contentType.indexOf("application/json") !== -1) {
    return response.json();
  } else {
    return null;
  }
}
export async function getOrders(token) {
  const requestOptions = {
    method: "GET",
  };

  if (token !== undefined) {
    requestOptions.headers = {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
    };
  }

  const response = await fetch(`${BACKEND_ADDRESS}/orders`, requestOptions);

  if (!response.ok) {
    if (response.status >= 200 && response.status < 500) {
      const res = await response.json();
      const detail = res["detail"];
      throw new Error(detail);
    }
    throw new Error("Service unavaliable!");
  }

  const contentType = response.headers.get("content-type");
  if (contentType && contentType.indexOf("application/json") !== -1) {
    return response.json();
  } else {
    return null;
  }
}

export async function getCategories() {
  const response = await fetch(`${BACKEND_ADDRESS}/categories`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    if (response.status >= 200 && response.status < 500) {
      const res = await response.json();
      const detail = res["detail"];
      throw new Error(detail);
    }
    throw new Error("Service unavaliable!");
  }

  const contentType = response.headers.get("content-type");
  if (contentType && contentType.indexOf("application/json") !== -1) {
    return response.json();
  } else {
    return null;
  }
}

export async function postOrderItems(orderData) {
  const token = orderData.token;
  delete orderData.token;

  const response = await fetch(`${BACKEND_ADDRESS}/orders`, {
    method: "POST",
    body: JSON.stringify(orderData),
    headers: {
      Authorization: "Bearer " + token,
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    if (response.status >= 200 && response.status < 500) {
      const res = await response.json();
      const detail = res["detail"];
      throw new Error(detail);
    }
    throw new Error("Service unavaliable!");
  }

  const contentType = response.headers.get("content-type");
  if (contentType && contentType.indexOf("application/json") !== -1) {
    return response.json();
  } else {
    return null;
  }
}
export async function postProductCreate(productCreateData) {
  const token = productCreateData.token;

  const response = await fetch(`${BACKEND_ADDRESS}/products`, {
    method: "POST",
    body: JSON.stringify(productCreateData),
    headers: {
      Authorization: "Bearer " + token,
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    if (response.status >= 200 && response.status < 500) {
      const res = await response.json();
      const detail = res["detail"];
      throw new Error(detail);
    }
    throw new Error("Service unavaliable!");
  }

  const contentType = response.headers.get("content-type");
  if (contentType && contentType.indexOf("application/json") !== -1) {
    return response.json();
  } else {
    return null;
  }
}
