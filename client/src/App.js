import logo from "./logo.svg";
import "./App.css";
import { API } from "./config";
function App() {
  const login = async () => {
    await fetch(`${API}/api/user/login`, {
      method: "post",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: "test", password: "test" }),
    });
  };
  const mock = async () => {
    const response = await fetch(`${API}/api/protected`, {
      credentials: "include",
    });
    const body = await response.json();
    console.log(body);
  };
  const logout = async () => {
    const response = await fetch(`${API}/api/user/logout`, {
      method: "post",
      credentials: "include",
    });
    const body = await response.json();
    console.log(body);
  };
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Environment: {process.env.NODE_ENV}</p>
        <button onClick={login}>Login</button>
        <button onClick={mock}>Mock API</button>
        <button onClick={logout}>Logout</button>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
