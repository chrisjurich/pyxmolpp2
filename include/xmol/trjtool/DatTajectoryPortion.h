#pragma once
#include "DATReader.h"

namespace xmol::trjtool {

class DatTrajectoryPortion : public xmol::trajectory::TrajectoryPortion {
public:
  DatTrajectoryPortion(const std::string& filename);
  void set_coordinates(xmol::polymer::frameIndex_t frameIndex,
                       const std::vector<std::pair<int, xmol::polymer::Atom*>>&
                           index_atoms) override;
  void set_coordinates(xmol::polymer::frameIndex_t frameIndex,
                       xmol::polymer::AtomSelection& atoms) override;
  xmol::polymer::frameIndex_t n_frames() const override;
  xmol::polymer::atomIndex_t n_atoms_per_frame() const override;
  bool match(const xmol::polymer::AtomSelection& atoms) const override;
  void close() override;

private:
  std::string m_filename;
  std::unique_ptr<std::ifstream> m_stream;
  std::unique_ptr<DATReader> m_reader;
};
}
