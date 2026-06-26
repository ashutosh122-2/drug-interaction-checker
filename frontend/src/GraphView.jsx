import ReactFlow from "reactflow";
import "reactflow/dist/style.css";

function GraphView({ nodes, edges }) {
  return (
    <div style={{ height: "400px", width: "100%", marginTop: "20px" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
      />
    </div>
  );
}

export default GraphView;