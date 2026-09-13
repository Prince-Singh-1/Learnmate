/**
 * PerformanceChart — Recharts-based mastery visualization.
 */

import { motion } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface PerformanceChartProps {
  data: Array<{ topic: string; mastery: number }>;
}

const COLORS = [
  "hsl(222.2, 47.4%, 11.2%)",
  "hsl(12, 76%, 61%)",
  "hsl(173, 58%, 39%)",
  "hsl(197, 37%, 24%)",
  "hsl(43, 74%, 66%)",
  "hsl(27, 87%, 67%)",
];

export function PerformanceChart({ data }: PerformanceChartProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.1 }}
    >
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Topic Mastery</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data} layout="vertical" margin={{ left: 20 }}>
              <CartesianGrid
                strokeDasharray="3 3"
                horizontal={false}
                stroke="hsl(214.3, 31.8%, 91.4%)"
              />
              <XAxis
                type="number"
                domain={[0, 1]}
                tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
                fontSize={12}
              />
              <YAxis
                type="category"
                dataKey="topic"
                width={120}
                fontSize={12}
              />
              <Tooltip
                formatter={(value: any) => [
                  `${(Number(value) * 100).toFixed(1)}%`,
                  "Mastery",
                ]}

                contentStyle={{
                  borderRadius: "8px",
                  border: "1px solid hsl(214.3, 31.8%, 91.4%)",
                }}
              />
              <Bar dataKey="mastery" radius={[0, 4, 4, 0]} barSize={24}>
                {data.map((_entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </motion.div>
  );
}
