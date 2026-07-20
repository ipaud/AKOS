import { useEffect, useState } from "react";

export function BudgetRow({ lines, onTotal }) {
  const [total, setTotal] = useState(0);

  // Derived state kept in a state variable and synced in an effect. The total
  // is a pure function of `lines` and needs neither.
  useEffect(() => {
    setTotal(lines.reduce((sum, l) => sum + l.amount, 0));
  }, [lines]);

  useEffect(() => {
    onTotal(total);
  });

  return <td>{total}</td>;
}
