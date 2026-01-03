export function createAPI(moduleName, config = {}) 
{
    const API_URL = `http://localhost:8000/${moduleName}`

    function getHeaders() {
        const token = localStorage.getItem("token");

        const headers = {
            "Content-Type": "application/json"
        };

        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        return headers;
    }

    async function sendJSON(method, data) 
    {
        const res = await fetch(API_URL,
        {
            method,
            headers: getHeaders(),
            body: JSON.stringify(data)
        });

        if (!res.ok) throw new Error(`Error in ${method}`);
        return await res.json();
    }

    return {
        async fetchAll()
        {
            const res = await fetch(API_URL, {
                headers: getHeaders()
            });
            if (!res.ok) throw new Error("No se pudieron obtener los datos");
            return await res.json();
        },
        async fetchMine() {
            const res = await fetch(`${API_URL}/my`, {
                headers: getHeaders()
            });
            if (!res.ok) throw new Error("No se pudieron obtener los datos");
            return await res.json();
        },
        async create(data)
        {
            return await sendJSON('POST', data);
        },
        async update(data)
        {
            return await sendJSON('PUT', data);
        },
        async remove(id)
        {
            return await sendJSON('DELETE', { id });
        }
    };
}