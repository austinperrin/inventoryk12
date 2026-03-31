import type { CSSProperties, DragEvent, ReactNode } from 'react';
import type { WidgetHeight, WidgetSurface, WidgetWidth } from '../types';
import { WidgetMenu } from './WidgetMenu';

type DashboardCardProps = {
  id: string;
  title: string;
  description: string;
  width: WidgetWidth;
  height: WidgetHeight;
  surface: WidgetSurface;
  openCardMenuId: string | null;
  onToggleMenu: (cardId: string) => void;
  onCloseMenu: () => void;
  onToast: (title: string, detail: string) => void;
  editMode: boolean;
  onRemove: (cardId: string) => void;
  draggable?: boolean;
  onDragStart?: (cardId: string, event: DragEvent<HTMLElement>) => void;
  onDragOver?: (cardId: string, event: DragEvent<HTMLElement>) => void;
  onDrop?: (cardId: string, event: DragEvent<HTMLElement>) => void;
  onDragEnd?: () => void;
  isDragOver?: boolean;
  isDragging?: boolean;
  placementStyle?: CSSProperties;
  children: ReactNode;
};

function widthClass(width: WidgetWidth): string {
  if (width === 4) {
    return 'workspace-dashboard-card--w4';
  }
  if (width === 2) {
    return 'workspace-dashboard-card--w2';
  }
  if (width === 3) {
    return 'workspace-dashboard-card--w3';
  }
  return 'workspace-dashboard-card--w1';
}

export function DashboardCard({
  id,
  title,
  description,
  width,
  height,
  surface,
  openCardMenuId,
  onToggleMenu,
  onCloseMenu,
  onToast,
  editMode,
  onRemove,
  draggable = false,
  onDragStart,
  onDragOver,
  onDrop,
  onDragEnd,
  isDragOver = false,
  isDragging = false,
  placementStyle,
  children,
}: DashboardCardProps) {
  return (
    <article
      className={`workspace-dashboard-card workspace-dashboard-card--${surface} ${widthClass(width)} workspace-dashboard-card--h-${height}${editMode ? ' is-editing' : ''}${isDragOver ? ' is-drag-over' : ''}${isDragging ? ' is-dragging' : ''}`}
      draggable={draggable}
      onDragStart={onDragStart ? (event) => onDragStart(id, event) : undefined}
      onDragOver={onDragOver ? (event) => onDragOver(id, event) : undefined}
      onDrop={onDrop ? (event) => onDrop(id, event) : undefined}
      onDragEnd={onDragEnd}
      style={placementStyle}
    >
      {editMode ? (
        <>
          <span className="workspace-dashboard-grip workspace-dashboard-corner-bubble workspace-dashboard-corner-bubble--move" aria-label="Drag to reorder" role="img">
            <svg viewBox="0 0 20 20">
              <path d="M10 2.8v14.4M2.8 10h14.4M10 2.8l-2 2M10 2.8l2 2M10 17.2l-2-2M10 17.2l2-2M2.8 10l2-2M2.8 10l2 2M17.2 10l-2-2M17.2 10l-2 2" />
            </svg>
          </span>
          <button
            type="button"
            className="workspace-dashboard-remove workspace-dashboard-corner-bubble workspace-dashboard-corner-bubble--remove"
            aria-label={`Remove ${title}`}
            onClick={() => onRemove(id)}
          >
            <svg viewBox="0 0 20 20" aria-hidden="true">
              <path d="M6 6l8 8M14 6l-8 8" />
            </svg>
          </button>
        </>
      ) : null}
      <div className="workspace-dashboard-card-head">
        <div className="workspace-dashboard-card-meta">
          <p className="workspace-card-kicker">{title}</p>
          <p className="workspace-analytics-description">{description}</p>
        </div>
        <div className="workspace-dashboard-card-actions">
          <WidgetMenu
            cardId={id}
            cardTitle={title}
            openCardMenuId={openCardMenuId}
            onToggle={onToggleMenu}
            onClose={onCloseMenu}
            onToast={onToast}
          />
        </div>
      </div>
      <div className="workspace-dashboard-card-body">{children}</div>
    </article>
  );
}
