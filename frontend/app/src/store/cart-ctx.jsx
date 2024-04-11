import React, { createContext, useContext, useEffect, useState } from "react";

const CART_STORAGE_KEY = "shopping_cart";

const ShoppingCartContext = createContext();

export const ShoppingCartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);

  useEffect(() => {
    const storedCartItems = localStorage.getItem(CART_STORAGE_KEY);
    if (storedCartItems) {
      setCartItems(JSON.parse(storedCartItems));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cartItems));
  }, [cartItems]);

  const addItemToCart = (item) => {
    const existingItemIndex = cartItems.findIndex(
      (cartItem) => cartItem.name === item.name
    );

    if (existingItemIndex !== -1) {
      const updatedCartItems = [...cartItems];
      updatedCartItems[existingItemIndex].quantity += item.quantity;
      updatedCartItems[existingItemIndex].sum =
        item.price * updatedCartItems[existingItemIndex].quantity;
      setCartItems(updatedCartItems);
    } else {
      const updatedCartItems = [
        ...cartItems,
        {
          ...item,
          quantity: item.quantity,
          price: item.price * item.quantity,
          sum: item.price * item.quantity,
        },
      ];
      setCartItems(updatedCartItems);
    }
  };

  const removeItemFromCart = (selectedName) => {
    const updatedCartItems = cartItems.filter(
      (item) => item.name !== selectedName
    );
    setCartItems(updatedCartItems);
  };

  const updateItemQuantity = (name, newQuantity) => {
    const updatedCartItems = cartItems.map((item) => {
      if (item.name === name) {
        return { ...item, quantity: newQuantity };
      }
      return item;
    });
    setCartItems(updatedCartItems);
  };

  const calculateTotalPrice = () => {
    return cartItems.reduce(
      (total, item) => total + item.price * item.quantity,
      0
    );
  };

  const contextValue = {
    cartItems,
    addItemToCart,
    removeItemFromCart,
    updateItemQuantity,
    calculateTotalPrice,
  };

  return (
    <ShoppingCartContext.Provider value={contextValue}>
      {children}
    </ShoppingCartContext.Provider>
  );
};

export const useShoppingCart = () => {
  return useContext(ShoppingCartContext);
};
