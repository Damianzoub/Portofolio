export function formatDate(iso: string){
    const d = new Date(iso);
    return new Intl.DateTimeFormat('en-GB',{
        year:"numeric",
        month:'short',
        day:'2-digit',
        timeZone:'UTC'
    }).format(d)
}