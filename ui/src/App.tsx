import React, { useState } from 'react';


type SearchResult = {
    text: string;
}

const MAX_RESULT_LENGTH = 500;

async function fetchSearchResults(query: string): Promise<SearchResult[]> {
    query = encodeURIComponent(query);
    const res = await fetch(
        `http://localhost:8000/api/search?query=${query}`,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        }
    )
    const j = await res.json()
    return j.results.map((r: string) => ({
        text: r,
    }));
}

function App() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<SearchResult[] | null>(null);
    const [loading, setLoading] = useState(false);
    const [expandIndices, setExpandIndices] = useState<Set<number>>(new Set());

    const onCollapse = (idx: number) => {
        const set2 = new Set(expandIndices);
        if (set2.has(idx)) {
            set2.delete(idx);
        }
        setExpandIndices(set2);
    };

    const onExpand = (idx: number) => {
        const set2 = new Set(expandIndices);
        set2.add(idx);
        setExpandIndices(set2);
    };

    const onSearch = async () => {
        setLoading(true);
        const results = await fetchSearchResults(query);
        setResults(results);
        setLoading(false);
        // collapse all
        setExpandIndices(new Set());
    };

    const makeHighlightedResultText = (text: string, collapsed: boolean) => {
        // TODO: hightlight the result text based on the words in the query
        return <div
            style={{
                whiteSpace: collapsed ? undefined : 'pre-wrap',
            }}
        >
            {text + (collapsed ? ' ' : '... ')}
        </div>
    };

    const makeResult = (r: SearchResult, idx: number) => {
        return <div
            key={idx}
            className='result'
        >
            {r.text.length > MAX_RESULT_LENGTH ?
                (
                    expandIndices.has(idx) ?
                        <>
                            {makeHighlightedResultText(r.text, false)}
                            <a
                                href='#'
                                className='collapse-link'
                                onClick={ev => {
                                    ev.preventDefault();
                                    onCollapse(idx);
                                }}
                            >collapse</a>
                        </> :
                        <>
                            {makeHighlightedResultText(r.text.slice(0, MAX_RESULT_LENGTH), true)}
                            <a
                                href='#'
                                className='expand-link'
                                onClick={ev => {
                                    ev.preventDefault();
                                    onExpand(idx);
                                }}
                            >expand</a>
                        </>
                ) :
                r.text
            }
        </div>;
    };

    return (
        <div className="App">
            <div className='search-box'>
                <form onSubmit={(ev) => {
                    ev.preventDefault();
                    onSearch();
                }}>
                    <input
                        className='search-input'
                        value={query}
                        onChange={ev => {
                            setQuery(ev.target.value);
                        }}
                    />
                    <button
                        className='search-button'
                    >
                        Search
                    </button>
                </form>
            </div>
            <div className='top-space'></div>
            <div
                className='results'
                style={{
                    opacity: loading ? 0.5 : 1,
                }}
            >
                {results == null ?
                    '' :
                    results.map(makeResult)
                }
            </div>
        </div>
    );
}

export default App;
