import React from 'react';

function Form() {
  return (
    <form>
      <label>Username:</label>
      <input type="text" />
      <label>Password:</label>
      <input type="password" />
      <button>Login</button>
    </form>
  );
}

export default Form;