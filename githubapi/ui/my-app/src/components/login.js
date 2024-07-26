import { React } from "react";

import { Button } from "flowbite-react";

function GithubIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
      <path d="M9 18c-4.51 2-5-2-7-2" />
    </svg>
  );
}

function MountainIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m8 3 4 8 5-5 5 15H2L8 3z" />
    </svg>
  );
}
// const [isAuthorized, setAuthorized] = useState(false);
function Login({ setAuthorized }) {
  const handleSubmit = async () => {
    console.log("Redirecting...");

    const apiUrl = `http://localhost:8000/login`;
    console.log("API URL:", apiUrl);

    try {
      window.location.href = apiUrl;
    } catch (error) {
      console.error("Error fetching data:", error);
      console.log("error");
    } finally {
      console.log("Finished submitting");
      setAuthorized = true;
    }
  };

  return (
    <div className="overscroll-none	flex min-h-fit flex-col">
      <header className="bg-black px-4 py-3 md:px-6 md:py-4">
        <div className="container mx-auto flex items-center justify-between">
          <a href="#" className="flex items-center gap-2" prefetch={false}>
            <MountainIcon className="h-6 w-6 text-primary-foreground" />
            <span className="text-white text-lg font-medium text-primary-foreground">
              GithubContri
            </span>
          </a>
          <p className="text-white hidden text-sm font-medium text-primary-foreground md:block">
            <a href="http://kanav-codes.vercel.app" target="_undefined">
              About me
            </a>
          </p>
        </div>
      </header>
      <main className="flex-1">
        <section className="container mx-auto flex min-h-fit items-center justify-center px-4 md:px-6">
          <div className="overscroll-none flex flex-grow h-[80dvh] items-center justify-center">
            <div className="mx-auto max-w-md space-y-6">
              <div className="space-y-2 text-center">
                <h1 className="text-black text-3xl font-bold">Welcome!</h1>
                <p className="text-muted-foreground">
                  Sign in to your account to continue.
                </p>
              </div>
              <Button
                variant="outline"
                className="w-full"
                onClick={handleSubmit}
              >
                <GithubIcon className="mr-2 h-5 w-5" />
                Sign in with GitHub
              </Button>
            </div>
          </div>
        </section>
      </main>
      <footer className="bg-black px-4 py-6 md:px-6 md:py-8">
        <div className="container mx-auto flex flex-col items-center justify-between gap-4 md:flex-row">
          <p className="text-white text-sm text-muted-foreground">
            &copy; created by Kanav
          </p>
          <nav className="flex items-center gap-4">
            <a
              href="#"
              className="text-white text-sm font-medium text-muted-foreground hover:underline hover:underline-offset-4"
              prefetch={false}
            ></a>
            <a
              href="#"
              className="text-white text-sm font-medium text-muted-foreground hover:underline hover:underline-offset-4"
              prefetch={false}
            ></a>
          </nav>
        </div>
      </footer>
    </div>
  );
}

export default Login;
