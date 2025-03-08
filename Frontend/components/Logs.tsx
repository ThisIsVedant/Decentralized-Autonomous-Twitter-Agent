export default function Logs({ logs }: { logs: string[] }) {
    return (
        <div className="p-6 border rounded-lg shadow">
            <h3 className="text-2xl font-semibold text-black">Status and Logs</h3>
            <h1 className="text-sm text-gray-500">Track your automation progress</h1>
            <div className="h-[400px] overflow-y-auto border rounded p-2">
                {logs.length === 0 ? (
                    <p className="text-sm text-gray-500">No logs yet...</p>
                ) : (
                    logs.map((log, index) => <p key={index} className="text-sm text-black">{log}</p>)
                )}
            </div>
        </div>
    );
}
