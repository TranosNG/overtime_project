import  React, { useState , useEffect } from 'react'

const Clock = () => {

    const [date, setDate] = useState(new Date());
    
    useEffect(() => {
        const timer = setInterval(()=>setDate(new Date()), 1000 )
        return function cleanup() {
            clearInterval(timer)
        }
    
    });

    return(
        <div>
          <span>{date.toLocaleDateString()}   </span>
          <span>{date.toLocaleTimeString()}</span>
        </div>
    )
}

export default Clock