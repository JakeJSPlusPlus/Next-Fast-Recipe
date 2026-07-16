import { LoginCardWithAuth0, LoginCardWithoutAuth0 } from "@/components/LoginCard";



export default async function Home() {
  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex flex-1 w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <LoginCardWithAuth0 />
      </div>
      </main>
    </div>
  );
}
