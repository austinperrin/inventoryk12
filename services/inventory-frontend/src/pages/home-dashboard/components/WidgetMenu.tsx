type WidgetMenuProps = {
  cardId: string;
  cardTitle: string;
  openCardMenuId: string | null;
  onToggle: (cardId: string) => void;
  onClose: () => void;
  onToast: (title: string, detail: string) => void;
};

function CardOptionsIcon() {
  return (
    <svg aria-hidden="true" className="workspace-card-options-icon" viewBox="0 0 24 24">
      <circle cx="12" cy="6.2" r="1.65" fill="currentColor" />
      <circle cx="12" cy="12" r="1.65" fill="currentColor" />
      <circle cx="12" cy="17.8" r="1.65" fill="currentColor" />
    </svg>
  );
}

export function WidgetMenu({ cardId, cardTitle, openCardMenuId, onToggle, onClose, onToast }: WidgetMenuProps) {
  const isOpen = openCardMenuId === cardId;

  return (
    <div className="workspace-widget-menu workspace-widget-menu--inline">
      <button
        className={`workspace-widget-options${isOpen ? ' is-open' : ''}`}
        type="button"
        aria-label={`More options for ${cardTitle}`}
        aria-expanded={isOpen}
        onClick={() => onToggle(cardId)}
      >
        <CardOptionsIcon />
      </button>
      {isOpen ? (
        <div className="workspace-widget-dropdown" role="menu" aria-label={`${cardTitle} options`}>
          <button
            className="workspace-widget-dropdown-item"
            type="button"
            role="menuitem"
            onClick={() => {
              onToast('Refreshing widget', `${cardTitle} data has been refreshed.`);
              onClose();
            }}
          >
            <span className="workspace-widget-dropdown-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24">
                <path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5" />
              </svg>
            </span>
            <span>Refresh</span>
          </button>
          <button
            className="workspace-widget-dropdown-item"
            type="button"
            role="menuitem"
            onClick={() => {
              onToast('Widget details', `Showing details for ${cardTitle}.`);
              onClose();
            }}
          >
            <span className="workspace-widget-dropdown-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="9" />
                <path d="M12 16v-4M12 8h.01" />
              </svg>
            </span>
            <span>View details</span>
          </button>
          <button
            className="workspace-widget-dropdown-item"
            type="button"
            role="menuitem"
            onClick={() => {
              onToast('Export queued', `${cardTitle} export is being prepared.`);
              onClose();
            }}
          >
            <span className="workspace-widget-dropdown-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24">
                <path d="M12 4v10M8.5 10.5 12 14l3.5-3.5M5 18h14" />
              </svg>
            </span>
            <span>Export</span>
          </button>
        </div>
      ) : null}
    </div>
  );
}
