"use client";
import Header from "@/components/Header";
import Actions from "@/components/Actions";
import Logs from "@/components/Logs";
import {useState} from "react";

export default function Home() {
  const [logs, setLogs] = useState<string[]>([]);

  return (
      <div className="container mx-auto p-4 px-24">
        <Header />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <Actions setLogs={setLogs} />
          <Logs logs={logs} />
        </div>

      </div>
  );
}
