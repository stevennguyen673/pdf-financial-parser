import React, { useRef, useEffect, useState } from "react";
import * as d3 from "d3";

export default function CirclePackingChart({ data, width = 600, height = 600 }) {
  const svgRef = useRef();
  const [tooltip, setTooltip] = useState({ visible: false, x: 0, y: 0, name: "", value: 0 });
  const [hoveredId, setHoveredId] = useState(null);

  // Add margin to prevent circles from being cut off
  const margin = 30;
  const innerWidth = width - 2 * margin;
  const innerHeight = height - 2 * margin;

  useEffect(() => {
    if (!data) return;

    d3.select(svgRef.current).selectAll("*").remove();

    const root = d3
      .hierarchy(data)
      .sum((d) => d.value)
      .sort((a, b) => b.value - a.value);

    d3.pack()
      .size([innerWidth, innerHeight])
      .padding(3)(root);

    const svg = d3.select(svgRef.current);

    // Assign a unique id to each node for hover effect
    let nodeId = 0;
    root.each((d) => { d.data._nodeId = nodeId++; });

    // Create a group and translate it by the margin
    const g = svg.append("g").attr("transform", `translate(${margin},${margin})`);

    const node = g
      .selectAll("g")
      .data(root.descendants())
      .join("g")
      .attr("transform", (d) => `translate(${d.x},${d.y})`)
      .attr("style", "cursor:pointer;");

    node
      .append("circle")
      .attr("r", (d) => d.r)
      .attr("fill", (d) => (d.children ? "#69b3a2" : "#40a9f3"))
      .attr("stroke", "#333")
      .attr("stroke-width", 1.5)
      .attr("opacity", (d) => (hoveredId === null || hoveredId === d.data._nodeId ? 1 : 0.7))
      .on("mousemove", function (event, d) {
        setTooltip({
          visible: true,
          x: event.clientX,
          y: event.clientY,
          name: d.data.name,
          value: d.data.value,
        });
        setHoveredId(d.data._nodeId);

        if (d.depth > 0) {
          d3.select(this.parentNode).raise();
          d3.select(this)
            .transition()
            .duration(300)
            .attr("r", d.r * 1.07);
        }
      })
      .on("mouseleave", function (event, d) {
        setTooltip({ ...tooltip, visible: false });
        setHoveredId(null);
        if (d.depth > 0) {
          d3.select(this)
            .transition()
            .duration(300)
            .attr("r", d.r);
        }
      });

    // Add labels for top-level nodes
    node
      .filter((d) => d.depth === 1)
      .append("text")
      .attr("text-anchor", "middle")
      .attr("dy", ".3em")
      .style("font-size", "14px")
      .style("pointer-events", "none")
      .text((d) => d.data.name);

    // eslint-disable-next-line
  }, [data, width, height, hoveredId]);

  return (
    <div style={{ position: "relative" }}>
      <svg ref={svgRef} width={width} height={height} />
      {tooltip.visible && (
        <div
          style={{
            position: "fixed",
            left: tooltip.x + 10,
            top: tooltip.y + 10,
            background: "rgba(0,0,0,0.8)",
            color: "#fff",
            padding: "6px 10px",
            borderRadius: "4px",
            pointerEvents: "none",
            zIndex: 10,
            fontSize: "14px",
          }}
        >
          <div><strong>{tooltip.name}</strong></div>
          {tooltip.value !== undefined && <div>Value: {tooltip.value}</div>}
        </div>
      )}
    </div>
  );
} 