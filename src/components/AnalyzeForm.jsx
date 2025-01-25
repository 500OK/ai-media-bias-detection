export default function AnalyzeForm() {
    return (
        <div className="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto">
                <div className="bg-white shadow-md rounded-lg p-6">
                    <h1 className="text-2xl font-bold mb-6">Text Analysis Form</h1>

                    <form className="space-y-6">
                        <div>
                            <label htmlFor="text" className="block text-sm font-medium text-gray-700">
                                Input Text
                            </label>
                            <div className="mt-1">
                                <textarea
                                    id="text"
                                    name="text"
                                    rows={10}
                                    className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 mt-1 block w-full sm:text-sm border border-gray-300 rounded-md p-3"
                                    placeholder="Enter your text here..."
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <button
                                type="submit"
                                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                            >
                                Analyze Text
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
} 