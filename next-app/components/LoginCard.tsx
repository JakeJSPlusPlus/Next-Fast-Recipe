import { auth0 } from "@/lib/auth0";
import LoginButton from "@/components/LoginButton";
import LogoutButton from "@/components/LogoutButton";
import Profile from "@/components/Profile";
import Image from "next/image";

const LoggedOutHeader: string = "Welcome to next-app"
const LoggedOutMessage: string = "Get started by logging in"

//change this to your production URL after deployment
const API_URL = process.env.API_BASE_URL

export async function LoginCardWithAuth0() {
  const session = await auth0.getSession();
  const user = session?.user;



  return (
    <div className="flex flex-col items-center bg-gray-300 dark:bg-gray-600 h-100 w-100 p-5 rounded-xl border border-black dark:border-white">
    {user ? (
      <>
        <h1 className="text-[22px] font-bold text-gray-900 tracking-tight">{user.name}</h1>
        <div>
          <Image src={user.picture ?? "/vercel.svg"} alt="profile" width={100} height={100} />
        </div>
        <div className="w-full h-px bg-gray-100" />
        <Profile />
        <LogoutButton />
      </>
    ) : (
      <div className="flex flex-col items-center">
        <Image src="/vercel.svg" alt="logo" width={100} height={100} />
        <h1 className="text-[17px] font-bold text-gray-900 dark:text-white tracking-tight pb-5">{LoggedOutHeader}</h1>
        <p className="text-[13px] text-gray-400 text-center leading-relaxed -mt-2">
          {LoggedOutMessage}
        </p>
        <div className="h-3" />
        <LoginButton />
      </div>
    )}
  </div>)
}

export async function LoginCardWithoutAuth0() {

  return (
    <div className="flex flex-col items-center bg-gray-300 dark:bg-gray-600 h-100 w-100 p-5 rounded-xl border border-black dark:border-white">
      <h1 className="text-[22px] font-bold text-gray-900 tracking-tight">{LoggedOutHeader}</h1>
      <form action={`${API_URL}/api/token/v1`} method="POST">
        <input id="username" name="username" type="text" placeholder="Username" className="w-full p-2 mb-4 rounded-xl border border-gray-300 dark:border-gray-600" />
        <input id="password" name="password" type="password" placeholder="Password" className="w-full p-2 mb-4 rounded-xl border border-gray-300 dark:border-gray-600" />
        <button type="submit" className="w-full p-2 rounded-xl bg-gray-900 text-white">Login</button>
      </form>
    </div>
  )
}
