import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const NavigateBack = () => {
  const navigate = useNavigate();
  useEffect(() => {
    navigate(-1);
  }, []);

  return <div></div>;
};

export default NavigateBack;

// import React, { useEffect } from "react";
// import { useNavigate } from "react-router-dom";

// const NavigateBack = () => {
//   const navigate = useNavigate();
//   // useEffect(() => {
//   //   navigate(-1);
//   //   // window.history.forward();
//   // }, []);

//   const handleClick = () => {
//     navigate(-1);
//   };

//   return (
//     <div className="cursor-pointer" onClick={handleClick}>
//       Back{" "}
//     </div>
//   );
// };

// export default NavigateBack;
