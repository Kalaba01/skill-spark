import React from "react";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export const showToast = (message, type = "success") => {
  if (type === "success") {
    toast.success(message, { position: "top-right", autoClose: 3000 });
  } else if (type === "error") {
    toast.error(message, { position: "top-right", autoClose: 3000 });
  } else if (type === "info") {
    toast.info(message, { position: "top-right", autoClose: 3000 });
  } else if (type === "warning") {
    toast.warning(message, { position: "top-right", autoClose: 3000 });
  }
};

function ToastNotification() {
  return <ToastContainer />;
}

export default ToastNotification;
